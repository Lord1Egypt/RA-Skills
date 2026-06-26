// ═══════════════════════════════════════════════════════════════════════════
// Code Provenance & Web of Trust — Type Definitions
// See design/23-provenance-trust.md for full specification
// ═══════════════════════════════════════════════════════════════════════════

import type { StakingTier } from './types';

// ─── Artifact Types ──────────────────────────────────────────────────────

/**
 * Artifact types that can be wrapped in a SignedEnvelope.
 */
export type ArtifactType =
  | 'prompt'
  | 'plugin'
  | 'skill'
  | 'service'
  | 'agent-template'
  | 'process'
  | 'fence-handler'
  | 'model-config'
  | 'domain-definition'
  | 'memory-fragment';

// ─── Author Identity ─────────────────────────────────────────────────────

/**
 * Public portion of the author's identity, sufficient for verification
 * without exposing private key material.
 */
export interface AuthorIdentity {
  /** Ed25519 public key (base64) — from KeyTriplet.pub */
  pub: string;
  /** 16-char fingerprint — from KeyTriplet.fingerprint */
  fingerprint: string;
  /** 16-dimensional resonance field — from KeyTriplet.resonance */
  resonance: number[];
}

// ─── Endorsement ─────────────────────────────────────────────────────────

/**
 * An endorsement from a co-signer who vouches for an artifact.
 */
export interface Endorsement {
  /** Public identity of the endorser */
  endorser: AuthorIdentity;
  /** Ed25519 signature over the envelope's contentHash */
  signature: string;
  /** Optional SEA co-signature */
  seaSignature?: string;
  /** Timestamp of endorsement (epoch ms) */
  timestamp: number;
  /** Free-text reason or review summary */
  comment?: string;
}

// ─── Resonance Proof ─────────────────────────────────────────────────────

/**
 * Resonance proof: prime-based semantic verification tying the artifact
 * content to the author's key material.
 */
export interface ResonanceProof {
  /** Prime factors used in the proof computation */
  primes: number[];
  /** Hash of (contentHash + primes + author.resonance + timestamp) */
  hash: string;
  /** When the proof was generated (epoch ms) */
  timestamp: number;
}

// ─── Capabilities ────────────────────────────────────────────────────────

/**
 * Capabilities an artifact may request at runtime.
 * Superset of PluginPermission from plugin-types.ts.
 */
export type Capability =
  | 'network:http'
  | 'fs:read'
  | 'fs:write'
  | 'store:read'
  | 'store:write'
  | 'dsn:identity'
  | 'dsn:register-tool'
  | 'dsn:register-service'
  | 'dsn:publish-observation'
  | 'dsn:gmf-write'
  | 'crypto:sign'
  | 'crypto:encrypt'
  | 'wallet:read'
  | 'wallet:transfer'
  | 'system:shell'
  | 'ui:notification'
  | 'ui:overlay';

// ─── Signed Envelope ─────────────────────────────────────────────────────

/**
 * SignedEnvelope<T> — the universal provenance wrapper.
 *
 * Every executable artifact in AlephNet is distributed inside one of these.
 * The envelope is immutable once signed; modifications produce a new envelope
 * with parentEnvelopeHash pointing to the original.
 */
export interface SignedEnvelope<T> {
  /** SHA-256 of the canonicalized JSON of `payload` (lowercase hex) */
  contentHash: string;

  /** The actual artifact content */
  payload: T;

  /** What kind of artifact this is */
  artifactType: ArtifactType;

  /** Public portion of the author's KeyTriplet */
  author: AuthorIdentity;

  /** Creation timestamp (epoch ms) */
  createdAt: number;

  /** Semver version string */
  version: string;

  /** Ed25519 signature over contentHash by author's private key */
  signature: string;

  /** Optional Gun.js SEA co-signature for dual-layer verification */
  seaSignature?: string;

  /** Prime-based semantic verification binding content to author */
  resonanceProof: ResonanceProof;

  /**
   * For forks or modifications: the contentHash of the parent envelope.
   * Forms a Merkle-like provenance chain.
   */
  parentEnvelopeHash?: string;

  /** Co-signer endorsements from other identities */
  endorsements: Endorsement[];

  /** Capabilities the artifact needs to function */
  requestedCapabilities: Capability[];
}

// ─── Trust Levels ────────────────────────────────────────────────────────

/**
 * Trust levels mapped from a computed numeric score.
 *
 * | Level     | Score Range | Meaning                          |
 * |-----------|-------------|----------------------------------|
 * | SELF      | ≥ 1.0       | User's own code                  |
 * | VOUCHED   | ≥ 0.7       | Endorsed by friends              |
 * | COMMUNITY | ≥ 0.4       | Verified by the network          |
 * | UNKNOWN   | ≥ 0.0       | Unverified or external           |
 * | REVOKED   | < 0.0       | Known-bad or revoked             |
 */
export type TrustLevel = 'SELF' | 'VOUCHED' | 'COMMUNITY' | 'UNKNOWN' | 'REVOKED';

/**
 * Breakdown of contributing trust factors.
 */
export interface TrustFactors {
  /** Whether Ed25519 + SEA + resonance signatures all passed */
  signatureValid: boolean;
  /** Normalized social graph distance (0.0–1.0) */
  socialDistance: number;
  /** Normalized author reputation (0.0–1.0) */
  authorReputation: number;
  /** Normalized staking tier score (0.0–1.0) */
  stakingTier: number;
  /** Normalized endorsement quality (0.0–1.0) */
  endorsementQuality: number;
  /** Coherence network consensus score (0.0–1.0) */
  coherenceScore: number;
}

/**
 * Complete trust assessment for an artifact.
 */
export interface TrustAssessment {
  /** Computed numeric score (-1.0 to 1.0) */
  score: number;
  /** Mapped trust level */
  level: TrustLevel;
  /** Breakdown of contributing factors */
  factors: TrustFactors;
  /** When this assessment was computed (epoch ms) */
  evaluatedAt: number;
  /** How long this assessment is valid (ms) */
  ttlMs: number;
}

// ─── Capability Gating ───────────────────────────────────────────────────

/** Decision outcome for a single capability check. */
export type CapabilityDecision = 'ALLOW' | 'CONFIRM' | 'DENY';

/** Result of checking a single capability against trust. */
export interface CapabilityCheckResult {
  decision: CapabilityDecision;
  reason?: string;
}

// ─── Trust Overrides ─────────────────────────────────────────────────────

/**
 * User-defined trust override, stored locally and never propagated to network.
 */
export interface TrustOverride {
  /** Target: specific author fingerprint or envelope contentHash */
  target:
    | { type: 'author'; fingerprint: string }
    | { type: 'artifact'; contentHash: string };
  /** Override trust level (bypasses computed score) */
  trustLevel?: TrustLevel;
  /** Per-capability overrides */
  capabilityOverrides?: Partial<Record<Capability, CapabilityDecision>>;
  /** When this override was set (epoch ms) */
  createdAt: number;
  /** Optional expiry (epoch ms) */
  expiresAt?: number;
}

// ─── Verification Result ─────────────────────────────────────────────────

/**
 * Result of verifying a SignedEnvelope's cryptographic integrity.
 */
export interface VerificationResult {
  /** Whether all signature checks passed */
  valid: boolean;
  /** Ed25519 signature check passed */
  ed25519Valid: boolean;
  /** SEA co-signature check passed (true if not present) */
  seaValid: boolean;
  /** Resonance proof check passed */
  resonanceValid: boolean;
  /** If invalid, human-readable description of what failed */
  error?: string;
}

// ─── Audit Events ────────────────────────────────────────────────────────

/**
 * Provenance-specific audit event types, compatible with the existing
 * AuditEvent infrastructure (see design/16-security.md).
 */
export type ProvenanceAuditEventType =
  | 'PROVENANCE_SIGNED'
  | 'PROVENANCE_VERIFIED'
  | 'PROVENANCE_FAILED'
  | 'PROVENANCE_SELF'
  | 'PROVENANCE_VOUCHED'
  | 'PROVENANCE_COMMUNITY'
  | 'PROVENANCE_UNKNOWN'
  | 'PROVENANCE_REVOKED'
  | 'PROVENANCE_ENDORSED'
  | 'TRUST_OVERRIDE_SET'
  | 'CAPABILITY_CONFIRMED'
  | 'CAPABILITY_DENIED'
  | 'CAPABILITY_BLOCKED';

// ─── Service Interfaces ──────────────────────────────────────────────────

/**
 * Service for creating, verifying, and endorsing signed envelopes.
 */
export interface ISignedEnvelopeService {
  /**
   * Create a signed envelope wrapping the given payload.
   * Signs with the current user's KeyTriplet.
   */
  create<T>(
    payload: T,
    artifactType: ArtifactType,
    version: string,
    capabilities: Capability[],
    parentEnvelopeHash?: string
  ): Promise<SignedEnvelope<T>>;

  /**
   * Verify a signed envelope's cryptographic integrity.
   * Checks Ed25519 signature, optional SEA co-signature, and resonance proof.
   */
  verify<T>(envelope: SignedEnvelope<T>): Promise<VerificationResult>;

  /**
   * Add the current user's endorsement to an envelope.
   * Returns a new envelope with the endorsement appended.
   */
  endorse<T>(envelope: SignedEnvelope<T>, comment?: string): Promise<SignedEnvelope<T>>;

  /**
   * Compute the deterministic canonical content hash for a payload.
   * Uses sorted-key JSON serialization → UTF-8 → SHA-256 → lowercase hex.
   */
  computeContentHash<T>(payload: T): string;
}

/**
 * Service for evaluating trust levels of signed envelopes.
 */
export interface ITrustEvaluator {
  /**
   * Evaluate the trust level of a signed envelope.
   * Returns a TrustAssessment with score, level, and factor breakdown.
   */
  evaluate<T>(envelope: SignedEnvelope<T>): Promise<TrustAssessment>;
}

/**
 * Service for gating capabilities based on trust assessment.
 */
export interface ITrustGate {
  /**
   * Check whether a capability is allowed for a given trust assessment.
   * Returns the decision and, for CONFIRM, a human-readable reason.
   */
  check(
    capability: Capability,
    trust: TrustAssessment
  ): CapabilityCheckResult;

  /**
   * Check all requested capabilities for an envelope.
   * Returns a map of capability → decision.
   */
  checkAll(
    envelope: SignedEnvelope<unknown>,
    trust: TrustAssessment
  ): Map<Capability, CapabilityCheckResult>;
}

/**
 * Service for resolving provenance chains via parentEnvelopeHash links.
 */
export interface IProvenanceChainResolver {
  /**
   * Walk the provenance chain from an envelope back to its root.
   * Returns the chain in order [root, ..., current].
   */
  resolve(contentHash: string): Promise<SignedEnvelope<unknown>[]>;

  /**
   * Get all forks of an envelope (envelopes that reference it as parent).
   */
  getForks(contentHash: string): Promise<SignedEnvelope<unknown>[]>;
}

// ─── Trust Cache Entry ───────────────────────────────────────────────────

/**
 * Internal cache entry for trust assessments.
 */
export interface TrustCacheEntry {
  assessment: TrustAssessment;
  /** Cache key: SHA-256(envelope.contentHash + currentUser.pub) */
  cacheKey: string;
  /** Absolute expiry time (epoch ms) */
  expiresAt: number;
}

// ─── Constants ───────────────────────────────────────────────────────────

/** TTL values for trust assessment cache per trust level (ms) */
export const TRUST_CACHE_TTL: Record<TrustLevel, number> = {
  SELF: Infinity,
  VOUCHED: 60 * 60 * 1000,         // 1 hour
  COMMUNITY: 15 * 60 * 1000,       // 15 minutes
  UNKNOWN: 5 * 60 * 1000,          // 5 minutes
  REVOKED: 24 * 60 * 60 * 1000,    // 24 hours
};

/** Weight factors for trust score computation */
export const TRUST_WEIGHTS = {
  socialDistance: 0.30,
  authorReputation: 0.20,
  stakingTier: 0.15,
  endorsementQuality: 0.20,
  coherenceScore: 0.15,
} as const;

/** Social graph distance → normalized score mapping */
export const SOCIAL_DISTANCE_SCORES: Record<number, number> = {
  0: 1.0,   // Self
  1: 0.8,   // Direct friend
  2: 0.5,   // Friend-of-friend
  3: 0.2,   // Distance 3
  // Distance 4+ → 0.0
};

/** StakingTier → normalized score mapping */
export const STAKING_TIER_SCORES: Record<string, number> = {
  Archon: 1.0,
  Magus: 0.75,
  Adept: 0.5,
  Neophyte: 0.25,
};

/** Trust level score thresholds */
export const TRUST_THRESHOLDS = {
  SELF: 1.0,
  VOUCHED: 0.7,
  COMMUNITY: 0.4,
  UNKNOWN: 0.0,
  // Anything below 0.0 is REVOKED
} as const;
