// ═══════════════════════════════════════════════════════════════════════════
// TrustEvaluator — Evaluates trust levels of signed envelopes
// See design/23-provenance-trust.md §4 (Phase 1)
// ═══════════════════════════════════════════════════════════════════════════

import type { StakingTier } from '../common/types';
import type {
  ITrustEvaluator,
  SignedEnvelope,
  TrustAssessment,
  TrustFactors,
  TrustLevel,
  TrustOverride,
  AuthorIdentity
} from '../common/trust-types';
import {
  TRUST_WEIGHTS,
  SOCIAL_DISTANCE_SCORES,
  STAKING_TIER_SCORES,
  TRUST_THRESHOLDS,
  TRUST_CACHE_TTL,
} from '../common/trust-types';
import type { SignedEnvelopeService } from './SignedEnvelopeService';

// ─── Provider Interfaces ─────────────────────────────────────────────────

/**
 * Provides social graph data for computing trust distance.
 */
export interface ISocialGraphProvider {
  getFriends(): Promise<Array<{ id: string; publicKey: string }>>;
  getFriendsOfFriend(friendPub: string): Promise<Array<{ id: string; publicKey: string }>>;
}

/**
 * Provides reputation, staking, and coherence data for trust scoring.
 */
export interface IReputationProvider {
  getReputation(publicKey: string): Promise<number>;
  getStakingTier(publicKey: string): Promise<StakingTier>;
  getCoherenceScore(contentHash: string): Promise<number>;
}

/**
 * Interface for DomainManager to decouple dependency.
 */
export interface IDomainManager {
    getCommonDomains(userId: string): Promise<string[]>;
}

// ─── Internal Cache Entry ────────────────────────────────────────────────

interface CacheEntry {
  assessment: TrustAssessment;
  expiresAt: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// TrustEvaluator
// ═══════════════════════════════════════════════════════════════════════════

export class TrustEvaluator implements ITrustEvaluator {
  private cache = new Map<string, CacheEntry>();
  private overrideMap = new Map<string, TrustOverride>();

  constructor(
    private readonly envelopeService: SignedEnvelopeService,
    private readonly ownIdentity: AuthorIdentity | null,
    private readonly socialGraph: ISocialGraphProvider,
    private readonly reputationProvider: IReputationProvider,
    private readonly domainManager: IDomainManager
  ) {}

  // ─── ITrustEvaluator ──────────────────────────────────────────────────

  /**
   * Evaluate the trust level of a signed envelope.
   *
   * Algorithm (design/23-provenance-trust.md §4.2):
   *   1. Signature gate — reject invalid signatures immediately
   *   2. Self check — own artifacts get SELF/1.0
   *   3. Override check — user-defined trust/block overrides
   *   4. Weighted scoring — social distance, reputation, endorsements, staking, coherence
   *   5. Level mapping — score → TrustLevel via TRUST_THRESHOLDS
   */
  async evaluate<T>(envelope: SignedEnvelope<T>): Promise<TrustAssessment> {
    // ── Cache Check ──────────────────────────────────────────────────
    const cached = this.cache.get(envelope.contentHash);
    if (cached && cached.expiresAt > Date.now()) {
      return cached.assessment;
    }

    // ── Step 1: Signature Gate ───────────────────────────────────────
    const verification = await this.envelopeService.verify(envelope);
    if (!verification.valid) {
      return this.finalize(envelope.contentHash, 'REVOKED', -1, {
        signatureValid: false,
        socialDistance: 0,
        authorReputation: 0,
        stakingTier: 0,
        endorsementQuality: 0,
        coherenceScore: 0,
      });
    }

    // ── Step 2: Self Check ───────────────────────────────────────────
    if (this.ownIdentity && envelope.author.pub === this.ownIdentity.pub) {
      return this.finalize(envelope.contentHash, 'SELF', 1.0, {
        signatureValid: true,
        socialDistance: 1.0,
        authorReputation: 1.0,
        stakingTier: 1.0,
        endorsementQuality: 1.0,
        coherenceScore: 1.0,
      });
    }

    // ── Step 3: Override Check ───────────────────────────────────────
    const override =
      this.findOverrideForArtifact(envelope.contentHash) ??
      this.findOverrideForAuthor(envelope.author.fingerprint);

    if (override && override.trustLevel !== undefined) {
      if (override.trustLevel === 'REVOKED') {
        return this.finalize(envelope.contentHash, 'REVOKED', -1.0, {
          signatureValid: true,
          socialDistance: 0,
          authorReputation: 0,
          stakingTier: 0,
          endorsementQuality: 0,
          coherenceScore: 0,
        });
      }
      // Any non-REVOKED trustLevel override → VOUCHED / 0.9
      return this.finalize(envelope.contentHash, 'VOUCHED', 0.9, {
        signatureValid: true,
        socialDistance: 0.9,
        authorReputation: 0.9,
        stakingTier: 0.9,
        endorsementQuality: 0.9,
        coherenceScore: 0.9,
      });
    }

    // ── Step 4: Weighted Score Computation ───────────────────────────
    const friends = await this.socialGraph.getFriends();

    // 4a: Social Distance (weight 0.30)
    const socialDistanceScore = await this.computeSocialDistance(
      envelope.author,
      friends
    );

    // 4b: Author Reputation (weight 0.20)
    const authorReputation = await this.reputationProvider.getReputation(
      envelope.author.pub
    );

    // 4c: Endorsements (weight 0.20)
    const endorsementScore = this.computeEndorsementScore(envelope, friends);

    // 4d: Staking Tier (weight 0.15)
    const tier: StakingTier = await this.reputationProvider.getStakingTier(
      envelope.author.pub
    );
    const stakingScore = STAKING_TIER_SCORES[tier] ?? 0;

    // 4e: Coherence Score (weight 0.15)
    const coherenceScore = await this.reputationProvider.getCoherenceScore(
      envelope.contentHash
    );

    // ── Step 5: Final Score ──────────────────────────────────────────
    const finalScore =
      socialDistanceScore * TRUST_WEIGHTS.socialDistance +
      authorReputation * TRUST_WEIGHTS.authorReputation +
      endorsementScore * TRUST_WEIGHTS.endorsementQuality +
      stakingScore * TRUST_WEIGHTS.stakingTier +
      coherenceScore * TRUST_WEIGHTS.coherenceScore;

    // ── Step 6: Level Determination ──────────────────────────────────
    const level = this.scoreToLevel(finalScore);

    const factors: TrustFactors = {
      signatureValid: true,
      socialDistance: socialDistanceScore,
      authorReputation,
      stakingTier: stakingScore,
      endorsementQuality: endorsementScore,
      coherenceScore,
    };

    return this.finalize(envelope.contentHash, level, finalScore, factors);
  }

  // ─── Override Management ──────────────────────────────────────────────

  async setOverride(override: TrustOverride): Promise<void> {
    const key = this.overrideKey(override);
    this.overrideMap.set(key, override);
  }

  async removeOverride(contentHash: string): Promise<void> {
    this.overrideMap.delete(contentHash);
  }

  async getOverrides(): Promise<TrustOverride[]> {
    return Array.from(this.overrideMap.values());
  }

  // ─── Cache Management ─────────────────────────────────────────────────

  clearCache(): void {
    this.cache.clear();
  }

  // ─── Private Helpers ──────────────────────────────────────────────────

  /**
   * Compute social distance score for an author.
   * Distance 1 (friend) → 0.8, distance 2 (FoF) → 0.5, else 0.0.
   */
  private async computeSocialDistance(
    author: { pub: string; fingerprint: string },
    friends: Array<{ id: string; publicKey: string }>
  ): Promise<number> {
    // Distance 1: direct friend
    const isFriend = friends.some(f => f.publicKey === author.pub);
    if (isFriend) {
      return SOCIAL_DISTANCE_SCORES[1] ?? 0;
    }

    // Check shared domains
    const commonDomains = await this.domainManager.getCommonDomains(author.fingerprint);
    if (commonDomains.length > 0) {
        return 0.6;
    }

    // Distance 2: friend-of-friend
    for (const friend of friends) {
      const fofs = await this.socialGraph.getFriendsOfFriend(friend.publicKey);
      if (fofs.some(fof => fof.publicKey === author.pub)) {
        return SOCIAL_DISTANCE_SCORES[2] ?? 0;
      }
    }

    // Unknown
    return 0;
  }

  /**
   * Compute endorsement quality score.
   * Base: min(1.0, endorsementCount / 5).
   * Bonus: +0.1 per friend endorser (capped at 1.0).
   */
  private computeEndorsementScore<T>(
    envelope: SignedEnvelope<T>,
    friends: Array<{ id: string; publicKey: string }>
  ): number {
    const count = envelope.endorsements.length;
    let score = Math.min(1.0, count / 5);

    // Bonus for friend endorsers
    const friendPubs = new Set(friends.map(f => f.publicKey));
    const friendEndorsers = envelope.endorsements.filter(e =>
      friendPubs.has(e.endorser.pub)
    );
    score += friendEndorsers.length * 0.1;

    return Math.min(1.0, score);
  }

  /**
   * Map a numeric score to a TrustLevel using TRUST_THRESHOLDS.
   */
  private scoreToLevel(score: number): TrustLevel {
    if (score >= TRUST_THRESHOLDS.SELF) return 'SELF';
    if (score >= TRUST_THRESHOLDS.VOUCHED) return 'VOUCHED';
    if (score >= TRUST_THRESHOLDS.COMMUNITY) return 'COMMUNITY';
    if (score >= TRUST_THRESHOLDS.UNKNOWN) return 'UNKNOWN';
    return 'REVOKED';
  }

  /**
   * Build a TrustAssessment, cache it, and return it.
   */
  private finalize(
    contentHash: string,
    level: TrustLevel,
    score: number,
    factors: TrustFactors
  ): TrustAssessment {
    const ttlMs = TRUST_CACHE_TTL[level];
    const now = Date.now();
    const assessment: TrustAssessment = {
      score,
      level,
      factors,
      evaluatedAt: now,
      ttlMs,
    };

    this.cache.set(contentHash, {
      assessment,
      expiresAt: now + (ttlMs === Infinity ? Number.MAX_SAFE_INTEGER : ttlMs),
    });

    return assessment;
  }

  /**
   * Find an override targeting a specific artifact contentHash.
   */
  private findOverrideForArtifact(contentHash: string): TrustOverride | undefined {
    for (const override of this.overrideMap.values()) {
      if (override.target.type === 'artifact' && override.target.contentHash === contentHash) {
        return override;
      }
    }
    return undefined;
  }

  /**
   * Find an override targeting a specific author fingerprint.
   */
  private findOverrideForAuthor(fingerprint: string): TrustOverride | undefined {
    for (const override of this.overrideMap.values()) {
      if (override.target.type === 'author' && override.target.fingerprint === fingerprint) {
        return override;
      }
    }
    return undefined;
  }

  /**
   * Derive a stable map key from a TrustOverride's target.
   */
  private overrideKey(override: TrustOverride): string {
    if (override.target.type === 'artifact') {
      return override.target.contentHash;
    }
    return `author:${override.target.fingerprint}`;
  }
}
