/**
 * Hashing Utilities
 * 
 * Common hashing operations that wrap crypto functions for convenience.
 * Provides consistent content-addressable storage patterns.
 */

import { sha256Hex, contentHash as baseContentHash } from './crypto';
import { HexString } from './types';

// Re-export contentHash from crypto (single source of truth)
export { contentHash } from './crypto';

// ═══════════════════════════════════════════════════════════════════════════
// CONTENT HASHING EXTENSIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Generate a content hash with a prefix (e.g., model name)
 */
export function prefixedContentHash(prefix: string, content: string): HexString {
  return sha256Hex(`${prefix}:${content}`);
}

/**
 * Hash an object by JSON stringifying it first
 */
export function objectHash(obj: unknown): HexString {
  return sha256Hex(JSON.stringify(obj));
}

/**
 * Stable hash for objects (sorted keys)
 */
export function stableObjectHash(obj: unknown): HexString {
  return sha256Hex(stableStringify(obj));
}

/**
 * Hash multiple items together
 */
export function combineHashes(...hashes: HexString[]): HexString {
  return sha256Hex(hashes.join(''));
}

// ═══════════════════════════════════════════════════════════════════════════
// SMF HASHING
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Generate a stable hash from an SMF vector
 */
export function smfHash(smf: number[], precision: number = 6): HexString {
  const normalized = smf.map(n => n.toFixed(precision)).join(',');
  return sha256Hex(normalized);
}

/**
 * Short SMF fingerprint (first 16 hex chars)
 */
export function smfFingerprint(smf: number[]): string {
  return smfHash(smf).slice(0, 16);
}

// ═══════════════════════════════════════════════════════════════════════════
// ID GENERATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Generate a prefixed ID
 */
export function generateId(prefix: string): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}-${timestamp}-${random}`;
}

/**
 * Generate a short random ID
 */
export function shortId(): string {
  return Math.random().toString(36).substring(2, 10);
}

/**
 * Generate a content-based ID (deterministic)
 */
export function contentId(content: string): string {
  return baseContentHash(content, 'default').slice(0, 16);
}

// ═══════════════════════════════════════════════════════════════════════════
// MERKLE TREE UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Merkle tree node
 */
export interface MerkleNode {
  hash: HexString;
  left?: MerkleNode;
  right?: MerkleNode;
  data?: string;
}

/**
 * Build a Merkle tree from leaves
 */
export function buildMerkleTree(leaves: string[]): MerkleNode | null {
  if (leaves.length === 0) return null;
  
  // Create leaf nodes
  let nodes: MerkleNode[] = leaves.map(data => ({
    hash: sha256Hex(data),
    data
  }));
  
  // Build tree bottom-up
  while (nodes.length > 1) {
    const nextLevel: MerkleNode[] = [];
    
    for (let i = 0; i < nodes.length; i += 2) {
      const left = nodes[i];
      const right = nodes[i + 1] || left; // Duplicate if odd
      
      nextLevel.push({
        hash: combineHashes(left.hash, right.hash),
        left,
        right: nodes[i + 1] ? right : undefined
      });
    }
    
    nodes = nextLevel;
  }
  
  return nodes[0];
}

/**
 * Get Merkle root hash from leaves
 */
export function merkleRoot(leaves: string[]): HexString | null {
  const tree = buildMerkleTree(leaves);
  return tree?.hash || null;
}

/**
 * Generate Merkle proof for a leaf
 */
export function getMerkleProof(leaves: string[], index: number): HexString[] {
  if (index >= leaves.length) return [];
  
  const proof: HexString[] = [];
  let nodes: HexString[] = leaves.map(l => sha256Hex(l));
  let currentIndex = index;
  
  while (nodes.length > 1) {
    const nextLevel: HexString[] = [];
    
    for (let i = 0; i < nodes.length; i += 2) {
      const left = nodes[i];
      const right = nodes[i + 1] || left;
      
      // If current index is in this pair, add sibling to proof
      if (i === currentIndex || i + 1 === currentIndex) {
        const siblingIndex = currentIndex % 2 === 0 ? currentIndex + 1 : currentIndex - 1;
        if (siblingIndex < nodes.length) {
          proof.push(nodes[siblingIndex]);
        }
      }
      
      nextLevel.push(combineHashes(left, right));
    }
    
    currentIndex = Math.floor(currentIndex / 2);
    nodes = nextLevel;
  }
  
  return proof;
}

/**
 * Verify a Merkle proof
 */
export function verifyMerkleProof(
  leaf: string,
  proof: HexString[],
  root: HexString,
  index: number
): boolean {
  let hash = sha256Hex(leaf);
  let currentIndex = index;
  
  for (const proofHash of proof) {
    if (currentIndex % 2 === 0) {
      hash = combineHashes(hash, proofHash);
    } else {
      hash = combineHashes(proofHash, hash);
    }
    currentIndex = Math.floor(currentIndex / 2);
  }
  
  return hash === root;
}

// ═══════════════════════════════════════════════════════════════════════════
// STABLE STRINGIFY
// ═══════════════════════════════════════════════════════════════════════════

/**
 * JSON stringify with sorted keys for deterministic hashing
 */
export function stableStringify(obj: unknown): string {
  if (obj === null || typeof obj !== 'object') {
    return JSON.stringify(obj);
  }
  
  if (Array.isArray(obj)) {
    return '[' + obj.map(stableStringify).join(',') + ']';
  }
  
  const sortedKeys = Object.keys(obj as Record<string, unknown>).sort();
  const pairs = sortedKeys.map(key => {
    const value = (obj as Record<string, unknown>)[key];
    return `${JSON.stringify(key)}:${stableStringify(value)}`;
  });
  
  return '{' + pairs.join(',') + '}';
}

// ═══════════════════════════════════════════════════════════════════════════
// CHECKSUM
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Calculate a simple checksum for quick integrity checks
 */
export function quickChecksum(data: string): string {
  let hash = 0;
  for (let i = 0; i < data.length; i++) {
    const char = data.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash).toString(16).padStart(8, '0');
}

/**
 * Verify checksum matches
 */
export function verifyChecksum(data: string, checksum: string): boolean {
  return quickChecksum(data) === checksum;
}
