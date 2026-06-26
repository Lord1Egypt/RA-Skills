import { createHash, randomBytes } from 'node:crypto';

/**
 * Deterministic 16-byte traceId from a session ID.
 * SHA-256(sessionId) → first 16 bytes → 32 hex chars.
 */
export function traceIdFromSession(sessionId: string): string {
  const hash = createHash('sha256').update(sessionId).digest();
  return hash.subarray(0, 16).toString('hex');
}

/**
 * Random 8-byte spanId → 16 hex chars.
 */
export function randomSpanId(): string {
  return randomBytes(8).toString('hex');
}
