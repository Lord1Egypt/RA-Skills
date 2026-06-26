import { MemoryStore } from "./MemoryStore";
import { VectorIndex } from "./VectorIndex";
import {
  CreateMemoryInput,
  MemoryFilter,
  MemoryManagerOptions,
  MemoryRecord,
  MemoryStats,
  UpdateMemoryInput,
  VectorSearchOptions,
  VectorSearchResult,
} from "./types";

export class MemoryManager {
  readonly store: MemoryStore;
  readonly vectorIndex: VectorIndex;

  constructor(options: MemoryManagerOptions = {}) {
    this.store = new MemoryStore(options.dbPath);
    this.vectorIndex = new VectorIndex(this.store);
  }

  create(input: CreateMemoryInput): MemoryRecord {
    return this.store.createMemory(input);
  }

  get(id: string): MemoryRecord | null {
    return this.store.getMemory(id);
  }

  update(id: string, input: UpdateMemoryInput): MemoryRecord | null {
    return this.store.updateMemory(id, input);
  }

  delete(id: string): boolean {
    return this.store.deleteMemory(id);
  }

  list(filter: MemoryFilter = {}): MemoryRecord[] {
    return this.store.listMemories(filter);
  }

  searchByVector(
    embedding: number[],
    options: VectorSearchOptions = {},
  ): VectorSearchResult[] {
    return this.vectorIndex.search(embedding, options);
  }

  listBySession(sessionId: string, limit = 100): MemoryRecord[] {
    return this.store.listMemories({ sessionId, limit });
  }

  listByUser(userId: string, limit = 100): MemoryRecord[] {
    return this.store.listMemories({ userId, limit });
  }

  cleanupExpired(referenceTime?: Date): number {
    return this.store.cleanupExpired(referenceTime);
  }

  stats(): MemoryStats {
    return this.store.getStats();
  }

  close(): void {
    this.store.close();
  }
}
