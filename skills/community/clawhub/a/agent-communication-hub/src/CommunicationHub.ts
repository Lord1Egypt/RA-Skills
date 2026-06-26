import { openDatabase, fromJson, createId, nowIso, toJson, type SqliteDatabase } from "./db.js";
import { EventBus } from "./EventBus.js";
import { SessionManager } from "./SessionManager.js";
import type { MessageKind, MessageQuery, MessageRecord, SendMessageInput } from "./types.js";

export interface CommunicationHubOptions {
  dbPath?: string;
  db?: SqliteDatabase;
}

export class CommunicationHub {
  public readonly db: SqliteDatabase;
  public readonly sessions: SessionManager;
  public readonly events: EventBus;

  public constructor(options: CommunicationHubOptions = {}) {
    this.db = options.db ?? openDatabase(options.dbPath ?? ":memory:");
    this.sessions = new SessionManager(this.db);
    this.events = new EventBus(this.db, this.sessions);
  }

  public sendDirectMessage(input: SendMessageInput): MessageRecord {
    if (!input.recipientId) {
      throw new Error("recipientId is required for direct messages");
    }

    return this.createMessage("direct", input.senderId, input.recipientId, input.payload, input.topic, input.correlationId);
  }

  public sendPrivateMessage(input: SendMessageInput): MessageRecord {
    if (!input.recipientId) {
      throw new Error("recipientId is required for private messages");
    }

    return this.createMessage("private", input.senderId, input.recipientId, input.payload, input.topic, input.correlationId);
  }

  public broadcastMessage(input: Omit<SendMessageInput, "recipientId">): MessageRecord[] {
    this.sessions.getAgent(input.senderId);
    const recipients = this.sessions
      .listAgents()
      .filter((agent) => agent.id !== input.senderId)
      .map((agent) => agent.id);

    return recipients.map((recipientId) =>
      this.createMessage("broadcast", input.senderId, recipientId, input.payload, input.topic, input.correlationId),
    );
  }

  public acknowledgeMessage(messageId: string): MessageRecord {
    const record = this.getMessage(messageId);
    const acknowledgedAt = nowIso();

    this.db
      .prepare(
        `UPDATE messages
         SET status = 'acknowledged', acknowledged_at = ?
         WHERE id = ?`,
      )
      .run(acknowledgedAt, messageId);

    return this.getMessage(messageId);
  }

  public drainOfflineQueue(agentId: string): MessageRecord[] {
    this.sessions.getAgent(agentId);
    if (!this.sessions.isAgentOnline(agentId)) {
      return [];
    }

    const deliveredAt = nowIso();
    this.db
      .prepare(
        `UPDATE messages
         SET status = 'delivered', delivered_at = ?
         WHERE recipient_id = ? AND status = 'pending'`,
      )
      .run(deliveredAt, agentId);

    return this.listMessages({ recipientId: agentId, status: "delivered" });
  }

  public getPendingMessages(agentId: string): MessageRecord[] {
    return this.listMessages({ recipientId: agentId, status: "pending" });
  }

  public listMessages(query: MessageQuery = {}): MessageRecord[] {
    const conditions: string[] = [];
    const values: Array<string | number> = [];

    if (query.senderId) {
      conditions.push("sender_id = ?");
      values.push(query.senderId);
    }
    if (query.recipientId) {
      conditions.push("recipient_id = ?");
      values.push(query.recipientId);
    }
    if (query.status) {
      conditions.push("status = ?");
      values.push(query.status);
    }
    if (query.kind) {
      conditions.push("kind = ?");
      values.push(query.kind);
    }

    const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
    const limit = query.limit ?? 100;
    const rows = this.db
      .prepare(`SELECT * FROM messages ${where} ORDER BY created_at DESC LIMIT ?`)
      .all(...values, limit) as Array<Record<string, string | null>>;

    return rows.map(mapMessageRow);
  }

  public close(): void {
    this.db.close();
  }

  private createMessage(
    kind: MessageKind,
    senderId: string,
    recipientId: string,
    payload: Record<string, unknown>,
    topic?: string,
    correlationId?: string,
  ): MessageRecord {
    this.sessions.getAgent(senderId);
    this.sessions.getAgent(recipientId);

    const recipientOnline = this.sessions.isAgentOnline(recipientId);
    const timestamp = nowIso();
    const messageId = createId("msg");
    const status = recipientOnline ? "delivered" : "pending";
    const deliveredAt = recipientOnline ? timestamp : null;

    this.db
      .prepare(
        `INSERT INTO messages (
           id, kind, sender_id, recipient_id, payload_json, status, topic,
           created_at, delivered_at, acknowledged_at, correlation_id
         )
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?)`,
      )
      .run(
        messageId,
        kind,
        senderId,
        recipientId,
        toJson(payload),
        status,
        topic ?? null,
        timestamp,
        deliveredAt,
        correlationId ?? null,
      );

    return this.getMessage(messageId);
  }

  private getMessage(messageId: string): MessageRecord {
    const row = this.db.prepare("SELECT * FROM messages WHERE id = ?").get(messageId) as Record<string, string | null> | undefined;
    if (!row) {
      throw new Error(`Message not found: ${messageId}`);
    }

    return mapMessageRow(row);
  }
}

function mapMessageRow(row: Record<string, string | null>): MessageRecord {
  return {
    id: row.id as string,
    kind: row.kind as MessageRecord["kind"],
    senderId: row.sender_id as string,
    recipientId: row.recipient_id as string | null,
    payload: fromJson(row.payload_json as string),
    status: row.status as MessageRecord["status"],
    topic: row.topic as string | null,
    createdAt: row.created_at as string,
    deliveredAt: row.delivered_at as string | null,
    acknowledgedAt: row.acknowledged_at as string | null,
    correlationId: row.correlation_id as string | null,
  };
}
