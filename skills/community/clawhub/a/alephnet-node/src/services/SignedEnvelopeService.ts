// ═══════════════════════════════════════════════════════════════════════════
// SignedEnvelopeService — Creates, verifies, and endorses signed envelopes
// See design/23-provenance-trust.md §2, §9 (Phase 1)
// ═══════════════════════════════════════════════════════════════════════════

import {
  base64ToBuffer,
  KeyTriplet,
  sha256Hex,
  signToBase64,
  verifyFromBase64
} from '../common/crypto';
import type {
  ArtifactType,
  AuthorIdentity,
  Capability,
  Endorsement,
  ISignedEnvelopeService,
  ResonanceProof,
  SignedEnvelope,
  VerificationResult,
} from '../common/trust-types';

/**
 * Interface for providing cryptographic identity.
 * Replaces the client-side IdentityManager dependency.
 */
export interface ICryptoProvider {
  getIdentity(): Promise<KeyTriplet | null>;
}

/**
 * Canonicalize an object for deterministic hashing.
 *
 * Algorithm (from design/23-provenance-trust.md §2.1):
 *   1. Deep-sort all object keys recursively
 *   2. Serialize to JSON
 *   3. The result is used as input to SHA-256
 */
function canonicalize(value: unknown): string {
  return JSON.stringify(sortKeysDeep(value));
}

/**
 * Recursively sort object keys for deterministic serialization.
 */
function sortKeysDeep(value: unknown): unknown {
  if (value === null || value === undefined) return value;
  if (Array.isArray(value)) return value.map(sortKeysDeep);
  if (typeof value === 'object') {
    const sorted: Record<string, unknown> = {};
    for (const key of Object.keys(value as Record<string, unknown>).sort()) {
      sorted[key] = sortKeysDeep((value as Record<string, unknown>)[key]);
    }
    return sorted;
  }
  return value;
}

/**
 * Generate the resonance proof hash.
 *
 * From design/23-provenance-trust.md §4.2.1:
 *   hash = SHA-256(contentHash + primes + resonance + timestamp)
 */
function computeResonanceHash(
  contentHash: string,
  primes: number[],
  resonance: number[],
  timestamp: number
): string {
  const input = `${contentHash}:${primes.join(',')}:${resonance.join(',')}:${timestamp}`;
  return sha256Hex(input);
}

/**
 * Select primes for the resonance proof from the author's bodyPrimes
 * and the content hash. If bodyPrimes are unavailable, derives primes
 * from the content hash deterministically.
 */
function selectResonancePrimes(contentHash: string, bodyPrimes?: number[]): number[] {
  if (bodyPrimes && bodyPrimes.length > 0) {
    // Use a subset of bodyPrimes seeded by the content hash
    const seed = parseInt(contentHash.substring(0, 8), 16);
    const count = Math.min(bodyPrimes.length, 8);
    const selected: number[] = [];
    for (let i = 0; i < count; i++) {
      selected.push(bodyPrimes[(seed + i) % bodyPrimes.length]);
    }
    return selected;
  }
  // Fallback: derive small primes from hash bytes
  const smallPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53];
  const indices: number[] = [];
  for (let i = 0; i < 8; i++) {
    const byte = parseInt(contentHash.substring(i * 2, i * 2 + 2), 16);
    indices.push(smallPrimes[byte % smallPrimes.length]);
  }
  return indices;
}

/**
 * Check resonance proof validity.
 *
 * From design/23-provenance-trust.md §4.2.1:
 *   - Proof primes must have ≥ 50% overlap with author's bodyPrimes
 *   - Proof hash must match SHA-256(contentHash + primes + resonance + timestamp)
 */
function verifyResonanceProof(
  proof: ResonanceProof,
  contentHash: string,
  author: AuthorIdentity,
  bodyPrimes?: number[]
): boolean {
  // 1. Verify the hash
  const expectedHash = computeResonanceHash(
    contentHash,
    proof.primes,
    author.resonance,
    proof.timestamp
  );
  if (proof.hash !== expectedHash) return false;

  // 2. Check prime overlap if bodyPrimes available
  if (bodyPrimes && bodyPrimes.length > 0) {
    const bodySet = new Set(bodyPrimes);
    const overlapping = proof.primes.filter(p => bodySet.has(p));
    const overlapRatio = overlapping.length / proof.primes.length;
    if (overlapRatio < 0.5) return false;
  }

  return true;
}

// ═══════════════════════════════════════════════════════════════════════════
// SignedEnvelopeService
// ═══════════════════════════════════════════════════════════════════════════

export class SignedEnvelopeService implements ISignedEnvelopeService {
  constructor(private readonly cryptoProvider: ICryptoProvider) {}

  /**
   * Compute the deterministic canonical content hash for a payload.
   *
   * Algorithm (design/23-provenance-trust.md §2.1):
   *   1. Serialize payload to JSON with sorted keys
   *   2. Encode as UTF-8 bytes
   *   3. Compute SHA-256
   *   4. Encode as lowercase hex
   */
  computeContentHash<T>(payload: T): string {
    const canonical = canonicalize(payload);
    return sha256Hex(canonical);
  }

  /**
   * Create a signed envelope wrapping the given payload.
   *
   * Flow (design/23-provenance-trust.md §9):
   *   1. Compute contentHash from canonical payload
   *   2. Sign contentHash with Ed25519 private key
   *   3. Generate resonanceProof binding content to author
   *   4. Assemble and return the SignedEnvelope
   */
  async create<T>(
    payload: T,
    artifactType: ArtifactType,
    version: string,
    capabilities: Capability[],
    parentEnvelopeHash?: string
  ): Promise<SignedEnvelope<T>> {
    const identity = await this.cryptoProvider.getIdentity();
    if (!identity) {
      throw new Error('No identity available. Create or import an identity first.');
    }

    // Step 1: Compute content hash
    const contentHash = this.computeContentHash(payload);

    // Step 2: Sign with Ed25519
    // Convert base64 private key to Buffer for signing
    const privKeyBuffer = base64ToBuffer(identity.priv);
    const signature = signToBase64(contentHash, privKeyBuffer);

    // Step 3: Generate resonance proof
    const now = Date.now();
    const primes = selectResonancePrimes(contentHash, identity.bodyPrimes);
    const resonanceProof: ResonanceProof = {
      primes,
      hash: computeResonanceHash(contentHash, primes, identity.resonance, now),
      timestamp: now,
    };

    // Step 4: Assemble the author identity (public portion only)
    const author: AuthorIdentity = {
      pub: identity.pub,
      fingerprint: identity.fingerprint,
      resonance: [...identity.resonance],
    };

    // Step 5: Build the envelope
    const envelope: SignedEnvelope<T> = {
      contentHash,
      payload,
      artifactType,
      author,
      createdAt: now,
      version,
      signature,
      resonanceProof,
      endorsements: [],
      requestedCapabilities: capabilities,
    };

    if (parentEnvelopeHash) {
      envelope.parentEnvelopeHash = parentEnvelopeHash;
    }

    return envelope;
  }

  /**
   * Verify a signed envelope's cryptographic integrity.
   *
   * Checks (design/23-provenance-trust.md §4.2.1):
   *   1. Ed25519 signature over contentHash using author.pub
   *   2. SEA co-signature (if present) — skipped if not present
   *   3. Resonance proof validity
   *   4. Content hash matches payload
   */
  async verify<T>(envelope: SignedEnvelope<T>): Promise<VerificationResult> {
    const result: VerificationResult = {
      valid: false,
      ed25519Valid: false,
      seaValid: true, // Default true when no SEA signature present
      resonanceValid: false,
    };

    // Step 0: Verify contentHash matches the actual payload
    const expectedHash = this.computeContentHash(envelope.payload);
    if (expectedHash !== envelope.contentHash) {
      result.error = 'Content hash mismatch: payload has been tampered with';
      return result;
    }

    // Step 1: Verify Ed25519 signature
    try {
      const pubKeyBuffer = base64ToBuffer(envelope.author.pub);
      result.ed25519Valid = verifyFromBase64(
        envelope.contentHash,
        envelope.signature,
        pubKeyBuffer
      );
    } catch (e) {
      result.ed25519Valid = false;
    }

    if (!result.ed25519Valid) {
      result.error = 'Ed25519 signature verification failed';
      return result;
    }

    // Step 2: Verify SEA co-signature (if present)
    if (envelope.seaSignature) {
      // SEA verification would go through Gun.SEA.verify — stubbed for Phase 1
      // For now, we accept it if present (SEA integration is Phase 2+)
      result.seaValid = true;
    }

    // Step 3: Verify resonance proof
    // Note: We don't have bodyPrimes from the author at verification time
    // (they're not in AuthorIdentity). We verify the hash only.
    // Full bodyPrimes overlap check requires looking up the author's profile.
    result.resonanceValid = verifyResonanceProof(
      envelope.resonanceProof,
      envelope.contentHash,
      envelope.author
    );
    if (!result.resonanceValid) {
      result.error = 'Resonance proof verification failed';
      return result;
    }

    // All checks passed
    result.valid = true;
    return result;
  }

  /**
   * Add the current user's endorsement to an envelope.
   *
   * Returns a new envelope (immutable pattern) with the endorsement appended.
   * The envelope's contentHash, signature, and resonanceProof remain unchanged —
   * endorsements are additive and don't alter the signed content.
   */
  async endorse<T>(envelope: SignedEnvelope<T>, comment?: string): Promise<SignedEnvelope<T>> {
    const identity = await this.cryptoProvider.getIdentity();
    if (!identity) {
      throw new Error('No identity available. Create or import an identity first.');
    }

    // Verify the envelope first — don't endorse invalid artifacts
    const verification = await this.verify(envelope);
    if (!verification.valid) {
      throw new Error(`Cannot endorse an invalid envelope: ${verification.error}`);
    }

    // Check we haven't already endorsed
    const alreadyEndorsed = envelope.endorsements.some(
      e => e.endorser.fingerprint === identity.fingerprint
    );
    if (alreadyEndorsed) {
      throw new Error('Current user has already endorsed this envelope');
    }

    // Sign the contentHash with our key
    const privKeyBuffer = base64ToBuffer(identity.priv);
    const endorsementSignature = signToBase64(envelope.contentHash, privKeyBuffer);

    const endorsement: Endorsement = {
      endorser: {
        pub: identity.pub,
        fingerprint: identity.fingerprint,
        resonance: [...identity.resonance],
      },
      signature: endorsementSignature,
      timestamp: Date.now(),
    };

    if (comment) {
      endorsement.comment = comment;
    }

    // Return new envelope with endorsement appended (immutable)
    return {
      ...envelope,
      endorsements: [...envelope.endorsements, endorsement],
    };
  }
}
