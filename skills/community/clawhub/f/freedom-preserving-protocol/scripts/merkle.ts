#!/usr/bin/env tsx
/**
 * merkle.ts
 *
 * SHA-256 Merkle tree utilities for the audit chain. Enables selective
 * disclosure: an agent can prove a specific audit entry exists without
 * revealing the full log (Law 1 — privacy by necessity).
 *
 * Exported functions:
 *   - computeMerkleRoot(leaves)     → root hash
 *   - createMerkleProof(leaves, i)  → sibling path + root
 *   - verifyMerkleProof(proof)      → boolean
 *
 * All hashing uses SHA-256 via @noble/hashes for consistency with the
 * rest of the audit chain.
 */

import { sha256 } from "@noble/hashes/sha256";
import { bytesToHex, utf8ToBytes } from "@noble/hashes/utils";

function hashPair(a: string, b: string): string {
  return bytesToHex(sha256(utf8ToBytes(a + b)));
}

export function computeMerkleRoot(leaves: string[]): string {
  if (leaves.length === 0) return "0".repeat(64);
  if (leaves.length === 1) return leaves[0];

  const level: string[] = [];
  for (let i = 0; i < leaves.length; i += 2) {
    const left = leaves[i];
    const right = leaves[i + 1] ?? left;
    level.push(hashPair(left, right));
  }
  return computeMerkleRoot(level);
}

export type MerkleProofStep = {
  hash: string;
  position: "left" | "right";
};

export type MerkleProof = {
  leaf: string;
  index: number;
  path: MerkleProofStep[];
  root: string;
};

export function createMerkleProof(
  leaves: string[],
  index: number,
): MerkleProof | null {
  if (index < 0 || index >= leaves.length || leaves.length === 0) return null;

  const path: MerkleProofStep[] = [];
  let currentLevel = [...leaves];
  let idx = index;

  while (currentLevel.length > 1) {
    if (currentLevel.length % 2 === 1) {
      currentLevel.push(currentLevel[currentLevel.length - 1]);
    }
    const siblingIdx = idx % 2 === 0 ? idx + 1 : idx - 1;
    path.push({
      hash: currentLevel[siblingIdx],
      position: idx % 2 === 0 ? "right" : "left",
    });

    const nextLevel: string[] = [];
    for (let i = 0; i < currentLevel.length; i += 2) {
      nextLevel.push(hashPair(currentLevel[i], currentLevel[i + 1]));
    }
    currentLevel = nextLevel;
    idx = Math.floor(idx / 2);
  }

  return {
    leaf: leaves[index],
    index,
    path,
    root: currentLevel[0],
  };
}

export function verifyMerkleProof(proof: MerkleProof): boolean {
  let current = proof.leaf;
  for (const step of proof.path) {
    current =
      step.position === "left"
        ? hashPair(step.hash, current)
        : hashPair(current, step.hash);
  }
  return current === proof.root;
}
