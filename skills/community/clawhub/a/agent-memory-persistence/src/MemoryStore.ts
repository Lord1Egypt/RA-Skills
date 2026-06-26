import Database from "better-sqlite3";
import { randomUUID } from "node:crypto";

import {
  CreateMemoryInput,
  MemoryFilter,
  MemoryRecord,
  MemoryStats,
  UpdateMemoryInput,
} from "./types";

type MemoryRow = {
  id: string;
  user_id: string | null;
  session_id: string | null;
  type: string;
  content: string;
  metadata_json: string | null;
  embedding_json: string | null;
  created_at: string;
  updated_at: string;
  expires_at: string | null;
};

function toIsoString(value?: string | Date | null): string | null {
  if (value === undefined) {
    return null;
  }
  if (value === null) {
    return null;
  }
  return value instanceof Date ? value.toISOString() : value;
}

function mapRow(row: MemoryRow): MemoryRecord {
  return {
    id: row.id,
    userId: row.user_id ?? undefined,
    sessionId: row.session_id ?? undefined,
    type: row.type,
    content: row.content,
    metadata: row.metadata_json ? JSON.parse(row.metadata_json) : undefined,
    embedding: row.embedding_json ? JSON.parse(row.embedding_json) : undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    expiresAt: row.expires_at ?? undefined,
  };
}

export class MemoryStore {
  private readonly db: Database.Database;

  constructor(dbPath = ":memory:") {
    this.db = new Database(dbPath);
    this.db.pragma("journal_mode = WAL");
    this.db.pragma("foreign_keys = ON");
    this.initialize();
  }

  private initialize(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS memories (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        session_id TEXT,
        type TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata_json TEXT,
        embedding_json TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        expires_at TEXT
      );

      CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories(user_id);
      CREATE INDEX IF NOT EXISTS idx_memories_session_id ON memories(session_id);
      CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
      CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at);
      CREATE INDEX IF NOT EXISTS idx_memories_expires_at ON memories(expires_at);
    `);
  }

  createMemory(input: CreateMemoryInput): MemoryRecord {
    const now = new Date().toISOString();
    const id = input.id ?? randomUUID();
    const type = input.type ?? "note";
    const expiresAt = toIsoString(input.expiresAt);
    const insert = this.db.prepare(`
      INSERT INTO memories (
        id, user_id, session_id, type, content, metadata_json,
        embedding_json, created_at, updated_at, expires_at
      ) VALUES (
        @id, @user_id, @session_id, @type, @content, @metadata_json,
        @embedding_json, @created_at, @updated_at, @expires_at
      )
    `);

    insert.run({
      id,
      user_id: input.userId ?? null,
      session_id: input.sessionId ?? null,
      type,
      content: input.content,
      metadata_json: input.metadata ? JSON.stringify(input.metadata) : null,
      embedding_json: input.embedding ? JSON.stringify(input.embedding) : null,
      created_at: now,
      updated_at: now,
      expires_at: expiresAt,
    });

    return this.getMemory(id)!;
  }

  getMemory(id: string): MemoryRecord | null {
    const row = this.db
      .prepare("SELECT * FROM memories WHERE id = ?")
      .get(id) as MemoryRow | undefined;

    return row ? mapRow(row) : null;
  }

  updateMemory(id: string, input: UpdateMemoryInput): MemoryRecord | null {
    const current = this.getMemory(id);
    if (!current) {
      return null;
    }

    const updated = {
      user_id: input.userId ?? current.userId ?? null,
      session_id: input.sessionId ?? current.sessionId ?? null,
      type: input.type ?? current.type,
      content: input.content ?? current.content,
      metadata_json:
        input.metadata !== undefined
          ? JSON.stringify(input.metadata)
          : current.metadata
            ? JSON.stringify(current.metadata)
            : null,
      embedding_json:
        input.embedding !== undefined
          ? JSON.stringify(input.embedding)
          : current.embedding
            ? JSON.stringify(current.embedding)
            : null,
      expires_at:
        input.expiresAt !== undefined
          ? toIsoString(input.expiresAt)
          : current.expiresAt ?? null,
      updated_at: new Date().toISOString(),
      id,
    };

    this.db
      .prepare(`
        UPDATE memories
        SET user_id = @user_id,
            session_id = @session_id,
            type = @type,
            content = @content,
            metadata_json = @metadata_json,
            embedding_json = @embedding_json,
            expires_at = @expires_at,
            updated_at = @updated_at
        WHERE id = @id
      `)
      .run(updated);

    return this.getMemory(id);
  }

  deleteMemory(id: string): boolean {
    const result = this.db
      .prepare("DELETE FROM memories WHERE id = ?")
      .run(id);
    return result.changes > 0;
  }

  listMemories(filter: MemoryFilter = {}): MemoryRecord[] {
    const clauses: string[] = [];
    const params: Record<string, unknown> = {};

    if (filter.ids?.length) {
      clauses.push(
        `id IN (${filter.ids.map((_, index) => `@id_${index}`).join(", ")})`,
      );
      filter.ids.forEach((id, index) => {
        params[`id_${index}`] = id;
      });
    }
    if (filter.userId) {
      clauses.push("user_id = @user_id");
      params.user_id = filter.userId;
    }
    if (filter.sessionId) {
      clauses.push("session_id = @session_id");
      params.session_id = filter.sessionId;
    }
    if (filter.type) {
      clauses.push("type = @type");
      params.type = filter.type;
    }
    if (filter.createdAfter) {
      clauses.push("created_at >= @created_after");
      params.created_after = toIsoString(filter.createdAfter);
    }
    if (filter.createdBefore) {
      clauses.push("created_at <= @created_before");
      params.created_before = toIsoString(filter.createdBefore);
    }
    if (!filter.includeExpired) {
      clauses.push("(expires_at IS NULL OR expires_at > @now)");
      params.now = new Date().toISOString();
    }

    const where = clauses.length ? `WHERE ${clauses.join(" AND ")}` : "";
    const limit = filter.limit ?? 100;
    const offset = filter.offset ?? 0;

    const rows = this.db
      .prepare(
        `
          SELECT *
          FROM memories
          ${where}
          ORDER BY created_at DESC
          LIMIT @limit OFFSET @offset
        `,
      )
      .all({
        ...params,
        limit,
        offset,
      }) as MemoryRow[];

    return rows.map(mapRow);
  }

  cleanupExpired(referenceTime = new Date()): number {
    const result = this.db
      .prepare("DELETE FROM memories WHERE expires_at IS NOT NULL AND expires_at <= ?")
      .run(referenceTime.toISOString());
    return result.changes;
  }

  getStats(): MemoryStats {
    const now = new Date().toISOString();
    const totalRow = this.db
      .prepare(
        `
          SELECT
            COUNT(*) as total,
            SUM(CASE WHEN expires_at IS NOT NULL AND expires_at <= @now THEN 1 ELSE 0 END) as expired,
            SUM(CASE WHEN embedding_json IS NOT NULL THEN 1 ELSE 0 END) as with_embeddings
          FROM memories
        `,
      )
      .get({ now }) as {
      total: number;
      expired: number | null;
      with_embeddings: number | null;
    };

    const byTypeRows = this.db
      .prepare("SELECT type, COUNT(*) as count FROM memories GROUP BY type")
      .all() as Array<{ type: string; count: number }>;

    return {
      total: totalRow.total,
      expired: totalRow.expired ?? 0,
      withEmbeddings: totalRow.with_embeddings ?? 0,
      byType: Object.fromEntries(byTypeRows.map((row) => [row.type, row.count])),
    };
  }

  close(): void {
    this.db.close();
  }
}
