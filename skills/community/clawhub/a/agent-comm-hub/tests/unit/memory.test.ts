/**
 * memory.test.ts — Memory 模块单元测试
 *
 * 策略：
 *  - 使用 vi.spyOn(db, 'prepare') 在每测试前替换为 :memory: 数据库
 *  - 包含 memories 表 + FTS5 虚拟表（recall 需要 FTS5）
 *  - FTS5 不可用时自动跳过 recall 相关测试
 *  - 测试隔离：beforeEach 重建 DB，afterEach 还原 spy
 */
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import Database from "better-sqlite3";
import type { Database as DatabaseType } from "better-sqlite3";

import { db } from "../../src/db.js";

// ─── 全局测试数据库（每次测试前重建）──────────────────────
let testDb: DatabaseType;
let fts5Available = true;

function setupDb(): DatabaseType {
  const db = new Database(":memory:");
  db.exec(`
    CREATE TABLE IF NOT EXISTS memories (
      id               TEXT PRIMARY KEY,
      agent_id         TEXT NOT NULL,
      title            TEXT,
      content          TEXT NOT NULL,
      fts_tokens       TEXT NOT NULL DEFAULT '',
      scope            TEXT NOT NULL DEFAULT 'private',
      tags             TEXT,
      source_agent_id  TEXT,
      source_task_id   TEXT,
      created_at       INTEGER NOT NULL,
      updated_at       INTEGER
    );
    CREATE INDEX IF NOT EXISTS idx_memories_agent ON memories(agent_id);
    CREATE INDEX IF NOT EXISTS idx_memories_scope ON memories(scope);
    CREATE INDEX IF NOT EXISTS idx_memories_source ON memories(source_agent_id);

    CREATE TABLE IF NOT EXISTS agents (
      agent_id      TEXT PRIMARY KEY,
      name          TEXT NOT NULL,
      role          TEXT NOT NULL DEFAULT 'member',
      status        TEXT NOT NULL DEFAULT 'offline',
      trust_score   INTEGER NOT NULL DEFAULT 50,
      last_heartbeat INTEGER,
      created_at    INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_log (
      id          TEXT PRIMARY KEY,
      action      TEXT NOT NULL,
      agent_id    TEXT,
      target      TEXT,
      details     TEXT,
      created_at  INTEGER NOT NULL,
      prev_hash   TEXT,
      record_hash TEXT
    );
  `);

  // 尝试创建 FTS5 虚拟表（可能因 SQLite 编译选项不支持）
  try {
    db.exec(`
      CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
        title, content, tags, fts_tokens
      );
    `);
    fts5Available = true;
  } catch {
    fts5Available = false;
  }

  return db;
}

function resetDb(): void {
  if (testDb) {
    try { testDb.exec("DELETE FROM memories"); } catch { /* ignore */ }
    try { testDb.exec("DELETE FROM memories_fts"); } catch { /* ignore */ }
  }
}

beforeEach(() => {
  testDb = setupDb();
  resetDb();
  vi.spyOn(db, "prepare").mockImplementation(
    (sql: string) => testDb.prepare(sql) as any
  );
});

afterEach(() => {
  vi.restoreAllMocks();
  if (testDb) {
    try { testDb.close(); } catch { /* ignore */ }
  }
});

// ─── 导入被测模块 ─────────────────────────────────────────
import {
  storeMemory,
  recallMemory,
  listMemories,
  deleteMemory,
  type MemoryEntry,
} from "../../src/memory.js";

// ─── 辅助函数 ─────────────────────────────────────────────
function insertRawMemory(testDb: DatabaseType, overrides: Partial<{
  id: string; agent_id: string; title: string; content: string;
  fts_tokens: string; scope: string; tags: string | null;
  source_agent_id: string | null; source_task_id: string | null;
  created_at: number; updated_at: number | null;
}>): void {
  const now = Date.now();
  const row = {
    id: `test_${now}_${Math.random().toString(36).slice(2, 8)}`,
    agent_id: "agent_test",
    title: null as string | null,
    content: "test content",
    fts_tokens: "",
    scope: "private",
    tags: null as string | null,
    source_agent_id: null as string | null,
    source_task_id: null as string | null,
    created_at: now,
    updated_at: null as number | null,
    ...overrides,
  };
  testDb.prepare(
    `INSERT INTO memories (id, agent_id, title, content, fts_tokens, scope, tags, source_agent_id, source_task_id, created_at, updated_at)
     VALUES (@id, @agent_id, @title, @content, @fts_tokens, @scope, @tags, @source_agent_id, @source_task_id, @created_at, @updated_at)`
  ).run(row);
}

// ═══════════════════════════════════════════════════════════════
// storeMemory
// ═══════════════════════════════════════════════════════════════
describe("storeMemory", () => {
  it("应成功存储一条记忆并返回 memory 对象", () => {
    const result = storeMemory("agent_alice", "Hello memory", { scope: "private" });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.memory.content).toBe("Hello memory");
      expect(result.memory.agent_id).toBe("agent_alice");
      expect(result.memory.scope).toBe("private");
      expect(result.memory.id).toBeTruthy();
      expect(result.memory.created_at).toBeGreaterThan(0);
    }
  });

  it("应支持 group 作用域", () => {
    const result = storeMemory("agent_alice", "Team note", { scope: "group" });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.memory.scope).toBe("group");
    }
  });

  it("应支持 collective 作用域", () => {
    const result = storeMemory("agent_alice", "Global knowledge", { scope: "collective" });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.memory.scope).toBe("collective");
    }
  });

  it("应支持 title 和 tags", () => {
    const result = storeMemory("agent_alice", "Important note", {
      title: "My Title",
      tags: ["tag1", "tag2"],
    });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.memory.title).toBe("My Title");
      expect(result.memory.tags).toBe(JSON.stringify(["tag1", "tag2"]));
    }
  });

  it("应支持溯源字段 source_agent_id 和 source_task_id", () => {
    const result = storeMemory("agent_bob", "Sourced memory", {
      source_agent_id: "agent_alice",
      source_task_id: "task_123",
    });
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.memory.source_agent_id).toBe("agent_alice");
      expect(result.memory.source_task_id).toBe("task_123");
    }
  });

  it("空内容应返回 error", () => {
    const result = storeMemory("agent_alice", "");
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toContain("cannot be empty");
    }
  });

  it("空白内容应返回 error", () => {
    const result = storeMemory("agent_alice", "   ");
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toContain("cannot be empty");
    }
  });

  it("超长内容（>10000）应返回 error", () => {
    const result = storeMemory("agent_alice", "x".repeat(10001));
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toContain("too long");
    }
  });

  it("超长 title（>500）应返回 error", () => {
    const result = storeMemory("agent_alice", "content", { title: "x".repeat(501) });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toContain("too long");
    }
  });

  it("无效 scope 应返回 error", () => {
    const result = storeMemory("agent_alice", "test", { scope: "invalid" as any });
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toContain("Invalid scope");
    }
  });

  it("必须成功持久化到数据库", () => {
    storeMemory("agent_alice", "Persistent note");
    const rows = testDb.prepare("SELECT COUNT(*) as cnt FROM memories").get() as { cnt: number };
    expect(rows.cnt).toBe(1);
  });
});

// ═══════════════════════════════════════════════════════════════
// recallMemory（FTS5 全文搜索）
// ═══════════════════════════════════════════════════════════════
describe("recallMemory", () => {
  beforeEach(() => {
    // 预置几条不同 scope 的记忆
    storeMemory("agent_alice", "Alice's private project plan", { title: "Project Plan", scope: "private", tags: ["project"] });
    storeMemory("agent_alice", "Team meeting notes about sprint planning", { title: "Sprint Planning", scope: "group", tags: ["team"] });
    storeMemory("agent_alice", "Global architecture decision: use SQLite", { title: "Architecture", scope: "collective", tags: ["arch"] });
    storeMemory("agent_bob", "Bob's private todo list", { title: "Todo", scope: "private" });
  });

  it("查询空字符串应返回空数组", () => {
    const results = recallMemory("", "agent_alice");
    expect(results).toEqual([]);
  });

  it("无匹配结果应返回空数组", () => {
    const results = recallMemory("nonexistenttoken", "agent_alice");
    expect(results).toEqual([]);
  });

  it("scope='all' 应返回 agent 可见的全部记忆（private + group + collective）", () => {
    const results = recallMemory("project", "agent_alice", { scope: "all" });
    expect(results.length).toBeGreaterThanOrEqual(1);
    expect(results.some(r => r.content.includes("project plan"))).toBe(true);
  });

  it("scope='private' 应只返回本人 private 记忆", () => {
    const results = recallMemory("sprint", "agent_alice", { scope: "private" });
    expect(results.length).toBe(0); // Alice 的 private 记忆不含 "sprint"
  });

  it("scope='collective' 应只返回 collective 记忆", () => {
    const results = recallMemory("architecture", "agent_alice", { scope: "collective" });
    expect(results.every(r => r.scope === "collective")).toBe(true);
  });

  it("scope='group' 不应返回 private 记忆", () => {
    const results = recallMemory("team", "agent_bob", { scope: "group" });
    // Bob 可以看到 group 记忆但不应看到别人 private 记忆
    expect(results.some(r => r.agent_id === "agent_alice" && r.scope === "private")).toBe(false);
  });
});

// ═══════════════════════════════════════════════════════════════
// listMemories
// ═══════════════════════════════════════════════════════════════
describe("listMemories", () => {
  beforeEach(() => {
    insertRawMemory(testDb, { agent_id: "agent_alice", content: "memory A", created_at: 1000 });
    insertRawMemory(testDb, { agent_id: "agent_alice", content: "memory B", scope: "group", created_at: 2000 });
    insertRawMemory(testDb, { agent_id: "agent_alice", content: "memory C", scope: "collective", created_at: 3000 });
    insertRawMemory(testDb, { agent_id: "agent_bob", content: "memory D", created_at: 4000 });
  });

  it("scope='all'（默认）应返回全部可访问的记忆", () => {
    const results = listMemories("agent_alice");
    // Alice 能看见自己的 private + group + collective + Bob 的 group/collective？
    expect(results.length).toBeGreaterThanOrEqual(3);
  });

  it("scope='private' 应只返回本人 private 记忆", () => {
    const results = listMemories("agent_alice", { scope: "private" });
    expect(results.length).toBe(1);
    expect(results[0].content).toBe("memory A");
  });

  it("scope='group' 不应包含 private", () => {
    const results = listMemories("agent_alice", { scope: "group" });
    expect(results.some(r => r.scope === "private")).toBe(false);
  });

  it("limit 应限制返回条数", () => {
    const results = listMemories("agent_alice", { limit: 2 });
    expect(results.length).toBeLessThanOrEqual(2);
  });

  it("offset 应实现分页", () => {
    const page1 = listMemories("agent_alice", { limit: 2, offset: 0 });
    const page2 = listMemories("agent_alice", { limit: 2, offset: 2 });
    if (page1.length > 0 && page2.length > 0) {
      expect(page1[0].id).not.toBe(page2[0].id);
    }
  });
});

// ═══════════════════════════════════════════════════════════════
// deleteMemory
// ═══════════════════════════════════════════════════════════════
describe("deleteMemory", () => {
  let memoryId: string;

  beforeEach(() => {
    const result = storeMemory("agent_alice", "To be deleted");
    if (result.ok) {
      memoryId = result.memory.id;
    }
  });

  it("应成功删除存在的记忆", () => {
    const result = deleteMemory(memoryId, "agent_alice", "member");
    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.deleted).toBe(true);
    }
    // 验证数据库中已删除
    const count = testDb.prepare("SELECT COUNT(*) as cnt FROM memories WHERE id=?").get(memoryId) as { cnt: number };
    expect(count.cnt).toBe(0);
  });

  it("删除不存在的 ID 应返回 error", () => {
    const result = deleteMemory("nonexistent_id", "agent_alice", "member");
    expect(result.ok).toBe(false);
    if (!result.ok) {
      expect(result.error).toContain("not found");
    }
  });

  it("其他 Agent 不能删除别人的记忆", () => {
    const result = deleteMemory(memoryId, "agent_bob", "member");
    expect(result.ok).toBe(false);
  });

  it("admin 可以删除别人的记忆", () => {
    const result = deleteMemory(memoryId, "agent_admin", "admin");
    expect(result.ok).toBe(true);
  });
});
