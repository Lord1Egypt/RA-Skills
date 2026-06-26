import type { EventPublishInput, EventRecord, EventReplayOptions, EventSubscription } from "./types.js";
import { createId, fromJson, nowIso, toJson, type SqliteDatabase } from "./db.js";
import { SessionManager } from "./SessionManager.js";

export class EventBus {
  public constructor(
    private readonly db: SqliteDatabase,
    private readonly sessions: SessionManager,
  ) {}

  public subscribe(agentId: string, eventType: string, filter: Record<string, unknown> = {}): EventSubscription {
    this.sessions.getAgent(agentId);

    const id = createId("sub");
    const createdAt = nowIso();
    this.db
      .prepare(
        `INSERT INTO event_subscriptions (id, agent_id, event_type, filter_json, created_at)
         VALUES (?, ?, ?, ?, ?)`,
      )
      .run(id, agentId, eventType, toJson(filter), createdAt);

    return { id, agentId, eventType, filter, createdAt };
  }

  public unsubscribe(subscriptionId: string): void {
    this.db.prepare("DELETE FROM event_subscriptions WHERE id = ?").run(subscriptionId);
  }

  public publish(input: EventPublishInput): { event: EventRecord; recipients: string[] } {
    if (input.sourceAgentId) {
      this.sessions.getAgent(input.sourceAgentId);
    }

    const event: EventRecord = {
      id: createId("evt"),
      type: input.type,
      sourceAgentId: input.sourceAgentId ?? null,
      payload: input.payload,
      metadata: input.metadata ?? {},
      createdAt: nowIso(),
    };

    this.db
      .prepare(
        `INSERT INTO events (id, type, source_agent_id, payload_json, metadata_json, created_at)
         VALUES (?, ?, ?, ?, ?, ?)`,
      )
      .run(
        event.id,
        event.type,
        event.sourceAgentId,
        toJson(event.payload),
        toJson(event.metadata),
        event.createdAt,
      );

    const rows = this.db
      .prepare("SELECT * FROM event_subscriptions WHERE event_type = ? ORDER BY created_at ASC")
      .all(event.type) as Array<Record<string, string>>;

    const recipients = rows
      .filter((row) => matchesFilter(fromJson(row.filter_json), event.payload))
      .map((row) => row.agent_id);

    return { event, recipients };
  }

  public replay(options: EventReplayOptions = {}): EventRecord[] {
    const conditions: string[] = [];
    const values: Array<string | number> = [];

    if (options.type) {
      conditions.push("type = ?");
      values.push(options.type);
    }
    if (options.sourceAgentId) {
      conditions.push("source_agent_id = ?");
      values.push(options.sourceAgentId);
    }
    if (options.since) {
      conditions.push("created_at >= ?");
      values.push(options.since);
    }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
    const limit = options.limit ?? 100;
    const sql = `SELECT * FROM events ${where} ORDER BY created_at DESC LIMIT ?`;
    const rows = this.db.prepare(sql).all(...values, limit) as Array<Record<string, string | null>>;

    return rows.map((row) => ({
      id: row.id as string,
      type: row.type as string,
      sourceAgentId: row.source_agent_id as string | null,
      payload: fromJson(row.payload_json as string),
      metadata: fromJson(row.metadata_json as string),
      createdAt: row.created_at as string,
    }));
  }

  public listSubscriptions(agentId?: string): EventSubscription[] {
    const rows = agentId
      ? (this.db
          .prepare("SELECT * FROM event_subscriptions WHERE agent_id = ? ORDER BY created_at ASC")
          .all(agentId) as Array<Record<string, string>>)
      : (this.db.prepare("SELECT * FROM event_subscriptions ORDER BY created_at ASC").all() as Array<Record<string, string>>);

    return rows.map((row) => ({
      id: row.id,
      agentId: row.agent_id,
      eventType: row.event_type,
      filter: fromJson(row.filter_json),
      createdAt: row.created_at,
    }));
  }
}

function matchesFilter(filter: Record<string, unknown>, payload: Record<string, unknown>): boolean {
  return Object.entries(filter).every(([key, value]) => payload[key] === value);
}
