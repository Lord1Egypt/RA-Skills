export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue };

export interface MemoryRecord {
  id: string;
  userId?: string;
  sessionId?: string;
  type: string;
  content: string;
  metadata?: Record<string, JsonValue>;
  embedding?: number[];
  createdAt: string;
  updatedAt: string;
  expiresAt?: string;
}

export interface CreateMemoryInput {
  id?: string;
  userId?: string;
  sessionId?: string;
  type?: string;
  content: string;
  metadata?: Record<string, JsonValue>;
  embedding?: number[];
  expiresAt?: string | Date;
}

export interface UpdateMemoryInput {
  content?: string;
  metadata?: Record<string, JsonValue>;
  embedding?: number[];
  expiresAt?: string | Date | null;
  type?: string;
  userId?: string;
  sessionId?: string;
}

export interface MemoryFilter {
  ids?: string[];
  userId?: string;
  sessionId?: string;
  type?: string;
  createdAfter?: string | Date;
  createdBefore?: string | Date;
  includeExpired?: boolean;
  limit?: number;
  offset?: number;
}

export interface VectorSearchOptions {
  userId?: string;
  sessionId?: string;
  type?: string;
  limit?: number;
  minScore?: number;
  includeExpired?: boolean;
}

export interface VectorSearchResult {
  memory: MemoryRecord;
  score: number;
}

export interface MemoryStats {
  total: number;
  expired: number;
  withEmbeddings: number;
  byType: Record<string, number>;
}

export interface MemoryManagerOptions {
  dbPath?: string;
}
