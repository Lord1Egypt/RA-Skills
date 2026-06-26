import { query } from "../db/db";
import type { WebhookEventRecord, WebhookEventRepository } from "./types";

/**
 * Postgres-backed webhook event repository.
 *
 * Idempotency is atomic: INSERT ... ON CONFLICT (idempotency_key) DO NOTHING.
 * If the insert returns 0 rows, the event was already processed.
 */
export class PostgresWebhookEventRepository implements WebhookEventRepository {
    async store(
        event: Omit<WebhookEventRecord, "id" | "processedAt">
    ): Promise<{ record: WebhookEventRecord; inserted: boolean }> {
        const rows = await query<{
            id: string;
            idempotency_key: string;
            event_type: string;
            payload: Record<string, unknown>;
            processed_at: Date;
        }>(
            `INSERT INTO webhook_events (idempotency_key, event_type, payload)
             VALUES ($1, $2, $3)
             ON CONFLICT (idempotency_key) DO NOTHING
             RETURNING id, idempotency_key, event_type, payload, processed_at`,
            [event.idempotencyKey, event.eventType, JSON.stringify(event.payload)]
        );

        // ON CONFLICT → duplicate, return existing
        if (rows.length === 0) {
            const existing = await this.findByIdempotencyKey(event.idempotencyKey);
            if (existing) return { record: existing, inserted: false };
            throw new Error(
                `Webhook event conflict for key=${event.idempotencyKey} but record not found`
            );
        }

        return { record: this.rowToRecord(rows[0]), inserted: true };
    }

    async findByIdempotencyKey(
        key: string
    ): Promise<WebhookEventRecord | undefined> {
        const rows = await query<{
            id: string;
            idempotency_key: string;
            event_type: string;
            payload: Record<string, unknown>;
            processed_at: Date;
        }>(
            `SELECT id, idempotency_key, event_type, payload, processed_at
             FROM webhook_events
             WHERE idempotency_key = $1`,
            [key]
        );

        return rows.length > 0 ? this.rowToRecord(rows[0]) : undefined;
    }

    // ── Row mapping ─────────────────────────────────────────

    private rowToRecord(row: {
        id: string;
        idempotency_key: string;
        event_type: string;
        payload: Record<string, unknown>;
        processed_at: Date;
    }): WebhookEventRecord {
        return {
            id: row.id,
            idempotencyKey: row.idempotency_key,
            eventType: row.event_type,
            payload: row.payload,
            processedAt: row.processed_at.toISOString()
        };
    }
}
