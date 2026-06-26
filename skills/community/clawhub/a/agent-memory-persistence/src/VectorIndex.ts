import { MemoryStore } from "./MemoryStore";
import { VectorSearchOptions, VectorSearchResult } from "./types";

function cosineSimilarity(left: number[], right: number[]): number {
  if (left.length === 0 || left.length !== right.length) {
    return -1;
  }

  let dot = 0;
  let leftNorm = 0;
  let rightNorm = 0;

  for (let index = 0; index < left.length; index += 1) {
    const leftValue = left[index]!;
    const rightValue = right[index]!;
    dot += leftValue * rightValue;
    leftNorm += leftValue * leftValue;
    rightNorm += rightValue * rightValue;
  }

  if (leftNorm === 0 || rightNorm === 0) {
    return -1;
  }

  return dot / (Math.sqrt(leftNorm) * Math.sqrt(rightNorm));
}

export class VectorIndex {
  constructor(private readonly store: MemoryStore) {}

  search(
    embedding: number[],
    options: VectorSearchOptions = {},
  ): VectorSearchResult[] {
    const candidates = this.store.listMemories({
      userId: options.userId,
      sessionId: options.sessionId,
      type: options.type,
      includeExpired: options.includeExpired,
      limit: 10_000,
    });

    const minScore = options.minScore ?? -1;
    const limit = options.limit ?? 10;

    return candidates
      .filter((memory) => Array.isArray(memory.embedding))
      .map((memory) => ({
        memory,
        score: cosineSimilarity(embedding, memory.embedding!),
      }))
      .filter((result) => result.score >= minScore)
      .sort((left, right) => right.score - left.score)
      .slice(0, limit);
  }
}
