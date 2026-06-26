import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

import { MemoryManager } from "../src";

function createManager(): { manager: MemoryManager; cleanup: () => void } {
  const dir = mkdtempSync(join(tmpdir(), "agent-memory-persistence-"));
  const dbPath = join(dir, "memory.db");
  const manager = new MemoryManager({ dbPath });

  return {
    manager,
    cleanup: () => {
      manager.close();
      rmSync(dir, { recursive: true, force: true });
    },
  };
}

test("stores and retrieves memory records with metadata and embeddings", () => {
  const { manager, cleanup } = createManager();

  try {
    const created = manager.create({
      userId: "user-1",
      sessionId: "session-1",
      type: "fact",
      content: "Alice likes black coffee",
      metadata: { topic: "preference", source: "chat" },
      embedding: [0.9, 0.1, 0.0],
    });

    const fetched = manager.get(created.id);
    assert.ok(fetched);
    assert.equal(fetched.content, "Alice likes black coffee");
    assert.equal(fetched.metadata?.topic, "preference");
    assert.deepEqual(fetched.embedding, [0.9, 0.1, 0.0]);
  } finally {
    cleanup();
  }
});

test("supports session filters, updates, vector search, and cleanup", () => {
  const { manager, cleanup } = createManager();

  try {
    const sessionMemory = manager.create({
      userId: "user-1",
      sessionId: "session-2",
      type: "summary",
      content: "The project uses SQLite for persistence",
      embedding: [1, 0, 0],
    });

    manager.create({
      userId: "user-1",
      sessionId: "session-2",
      type: "summary",
      content: "Semantic search uses cosine similarity",
      embedding: [0.95, 0.05, 0],
    });

    manager.create({
      userId: "user-2",
      sessionId: "session-9",
      type: "note",
      content: "Unrelated memory",
      embedding: [0, 1, 0],
      expiresAt: "2020-01-01T00:00:00.000Z",
    });

    const updated = manager.update(sessionMemory.id, {
      metadata: { reviewed: true },
      content: "The project uses SQLite for long-term persistence",
    });

    assert.ok(updated);
    assert.equal(updated.metadata?.reviewed, true);
    assert.match(updated.content, /long-term persistence/);

    const sessionItems = manager.listBySession("session-2");
    assert.equal(sessionItems.length, 2);

    const searchResults = manager.searchByVector([0.98, 0.02, 0], {
      userId: "user-1",
      limit: 2,
      minScore: 0.9,
    });

    assert.equal(searchResults.length, 2);
    assert.match(searchResults[0]!.memory.content, /SQLite|Semantic search/);
    assert.ok(searchResults[0]!.score >= searchResults[1]!.score);

    const removed = manager.cleanupExpired(new Date("2026-01-01T00:00:00.000Z"));
    assert.equal(removed, 1);

    const stats = manager.stats();
    assert.equal(stats.total, 2);
    assert.equal(stats.withEmbeddings, 2);
    assert.equal(stats.byType.summary, 2);
  } finally {
    cleanup();
  }
});
