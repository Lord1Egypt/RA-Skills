import type { AgentRecord, AgentRegistrationInput, SessionConnectInput, SessionRecord } from "./types.js";
import { createId, fromJson, nowIso, toJson, type SqliteDatabase } from "./db.js";

export class SessionManager {
  public constructor(private readonly db: SqliteDatabase) {}

  public registerAgent(input: AgentRegistrationInput): AgentRecord {
    const existing = this.db
      .prepare("SELECT * FROM agents WHERE id = ?")
      .get(input.id) as Record<string, string> | undefined;

    const timestamp = nowIso();
    const metadata = input.metadata ?? {};
    const name = input.name ?? input.id;

    if (existing) {
      this.db
        .prepare(
          `UPDATE agents
           SET name = ?, metadata_json = ?, updated_at = ?, last_seen_at = ?
           WHERE id = ?`,
        )
        .run(name, toJson(metadata), timestamp, timestamp, input.id);
    } else {
      this.db
        .prepare(
          `INSERT INTO agents (id, name, status, metadata_json, last_seen_at, created_at, updated_at)
           VALUES (?, ?, 'offline', ?, ?, ?, ?)`,
        )
        .run(input.id, name, toJson(metadata), timestamp, timestamp, timestamp);
    }

    return this.getAgent(input.id);
  }

  public connectAgent(input: SessionConnectInput): SessionRecord {
    this.ensureAgentExists(input.agentId);
    const sessionId = createId("session");
    const timestamp = nowIso();

    this.db
      .prepare(
        `INSERT INTO sessions (id, agent_id, status, connected_at, disconnected_at, metadata_json)
         VALUES (?, ?, 'connected', ?, NULL, ?)`,
      )
      .run(sessionId, input.agentId, timestamp, toJson(input.metadata ?? {}));

    this.db
      .prepare(
        `UPDATE agents
         SET status = 'online', last_seen_at = ?, updated_at = ?
         WHERE id = ?`,
      )
      .run(timestamp, timestamp, input.agentId);

    return this.getSession(sessionId);
  }

  public disconnectAgent(agentId: string): void {
    this.ensureAgentExists(agentId);
    const timestamp = nowIso();

    this.db
      .prepare(
        `UPDATE sessions
         SET status = 'disconnected', disconnected_at = ?
         WHERE agent_id = ? AND status = 'connected'`,
      )
      .run(timestamp, agentId);

    this.db
      .prepare(
        `UPDATE agents
         SET status = 'offline', last_seen_at = ?, updated_at = ?
         WHERE id = ?`,
      )
      .run(timestamp, timestamp, agentId);
  }

  public getAgent(agentId: string): AgentRecord {
    const row = this.db.prepare("SELECT * FROM agents WHERE id = ?").get(agentId) as Record<string, string> | undefined;
    if (!row) {
      throw new Error(`Agent not found: ${agentId}`);
    }

    return {
      id: row.id,
      name: row.name,
      status: row.status as AgentRecord["status"],
      metadata: fromJson(row.metadata_json),
      lastSeenAt: row.last_seen_at,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    };
  }

  public listAgents(): AgentRecord[] {
    const rows = this.db.prepare("SELECT * FROM agents ORDER BY created_at ASC").all() as Array<Record<string, string>>;
    return rows.map((row) => ({
      id: row.id,
      name: row.name,
      status: row.status as AgentRecord["status"],
      metadata: fromJson(row.metadata_json),
      lastSeenAt: row.last_seen_at,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    }));
  }

  public getSessionHistory(agentId: string): SessionRecord[] {
    this.ensureAgentExists(agentId);
    const rows = this.db
      .prepare("SELECT * FROM sessions WHERE agent_id = ? ORDER BY connected_at DESC")
      .all(agentId) as Array<Record<string, string | null>>;

    return rows.map((row) => ({
      id: row.id as string,
      agentId: row.agent_id as string,
      status: row.status as SessionRecord["status"],
      connectedAt: row.connected_at as string,
      disconnectedAt: row.disconnected_at as string | null,
      metadata: fromJson(row.metadata_json as string),
    }));
  }

  public isAgentOnline(agentId: string): boolean {
    return this.getAgent(agentId).status === "online";
  }

  private getSession(sessionId: string): SessionRecord {
    const row = this.db.prepare("SELECT * FROM sessions WHERE id = ?").get(sessionId) as Record<string, string | null> | undefined;
    if (!row) {
      throw new Error(`Session not found: ${sessionId}`);
    }

    return {
      id: row.id as string,
      agentId: row.agent_id as string,
      status: row.status as SessionRecord["status"],
      connectedAt: row.connected_at as string,
      disconnectedAt: row.disconnected_at as string | null,
      metadata: fromJson(row.metadata_json as string),
    };
  }

  private ensureAgentExists(agentId: string): void {
    const count = this.db.prepare("SELECT COUNT(*) as count FROM agents WHERE id = ?").get(agentId) as { count: number };
    if (count.count === 0) {
      throw new Error(`Agent not registered: ${agentId}`);
    }
  }
}
