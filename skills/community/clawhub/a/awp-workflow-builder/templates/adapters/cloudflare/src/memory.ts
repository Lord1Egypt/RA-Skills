// AWP Memory Manager for Cloudflare Workers
// Maps AWP memory tiers to Cloudflare services: KV, D1, R2.

import type { Env } from "./types";

/**
 * Memory manager that maps AWP's 3-tier memory model to Cloudflare services.
 *
 * - Working Memory:  JS variables (request-scoped, ephemeral)
 * - Short-term:      D1 (SQLite) — daily logs, queryable
 * - Long-term:       R2 (Object Storage) — MEMORY.md, unlimited
 */
export class MemoryManager {
  private env: Env;
  private workflowName: string;

  constructor(env: Env, workflowName: string) {
    this.env = env;
    this.workflowName = workflowName;
  }

  // ── Long-term Memory (R2) ──────────────────────────────────

  /** Read MEMORY.md for an agent from R2. Returns empty string if not found. */
  async readLongTerm(agentId: string): Promise<string> {
    if (!this.env.MEMORY) return "";
    const key = `${this.workflowName}/${agentId}/MEMORY.md`;
    const obj = await this.env.MEMORY.get(key);
    return obj ? await obj.text() : "";
  }

  /** Write/update MEMORY.md for an agent in R2. */
  async writeLongTerm(agentId: string, content: string): Promise<void> {
    if (!this.env.MEMORY) return;
    const key = `${this.workflowName}/${agentId}/MEMORY.md`;
    await this.env.MEMORY.put(key, content);
  }

  // ── Short-term Memory / Daily Logs (D1) ────────────────────

  /** Write a daily log entry for an agent. */
  async writeDailyLog(
    agentId: string,
    entry: string,
    date?: string,
  ): Promise<void> {
    if (!this.env.DB) return;
    const d = date ?? new Date().toISOString().split("T")[0];
    await this.env.DB.prepare(
      `INSERT INTO daily_logs (agent_id, date, entry, created_at)
       VALUES (?, ?, ?, datetime('now'))`,
    )
      .bind(agentId, d, entry)
      .run();
  }

  /** Read daily log entries for an agent, optionally filtered by date. */
  async readDailyLogs(
    agentId: string,
    date?: string,
  ): Promise<Array<{ date: string; entry: string }>> {
    if (!this.env.DB) return [];
    let stmt;
    if (date) {
      stmt = this.env.DB.prepare(
        `SELECT date, entry FROM daily_logs WHERE agent_id = ? AND date = ? ORDER BY created_at DESC`,
      ).bind(agentId, date);
    } else {
      stmt = this.env.DB.prepare(
        `SELECT date, entry FROM daily_logs WHERE agent_id = ? ORDER BY created_at DESC LIMIT 50`,
      ).bind(agentId);
    }
    const result = await stmt.all<{ date: string; entry: string }>();
    return result.results ?? [];
  }

  /** Search daily logs by keyword. */
  async searchDailyLogs(
    agentId: string,
    query: string,
  ): Promise<Array<{ date: string; entry: string }>> {
    if (!this.env.DB) return [];
    const stmt = this.env.DB.prepare(
      `SELECT date, entry FROM daily_logs WHERE agent_id = ? AND entry LIKE ? ORDER BY created_at DESC LIMIT 20`,
    ).bind(agentId, `%${query}%`);
    const result = await stmt.all<{ date: string; entry: string }>();
    return result.results ?? [];
  }

  // ── State (KV) ─────────────────────────────────────────────

  /** Save workflow state (agent outputs) to KV. */
  async saveState(
    runId: string,
    state: Record<string, unknown>,
  ): Promise<void> {
    const key = `state:${this.workflowName}:${runId}`;
    await this.env.STATE.put(key, JSON.stringify(state), {
      expirationTtl: 86400, // 24 hours
    });
  }

  /** Load workflow state from KV. */
  async loadState(
    runId: string,
  ): Promise<Record<string, unknown> | null> {
    const key = `state:${this.workflowName}:${runId}`;
    const data = await this.env.STATE.get(key);
    return data ? JSON.parse(data) : null;
  }

  // ── Database Initialization ────────────────────────────────

  /** Create required D1 tables if they don't exist. */
  async initDatabase(): Promise<void> {
    if (!this.env.DB) return;
    await this.env.DB.prepare(
      `CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL,
        date TEXT NOT NULL,
        entry TEXT NOT NULL,
        created_at TEXT NOT NULL
      )`,
    ).run();
  }
}
