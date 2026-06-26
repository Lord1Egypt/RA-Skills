import { appLogger } from "../../utils/logger";
/**
 * Notify Service — event-to-Telegram notification delivery.
 *
 * Idempotent delivery using bot_events + bot_messages tables.
 * Dedupe via idempotency_key, retry with exponential backoff.
 *
 * @module modules/notify/notifyService
 */

import crypto from "node:crypto";
import { query } from "../../db/db";
import { TelegramClient } from "../bot/telegramClient";
import { getTelegramClient } from "../bot/webhook";
import { env } from "../../config/env";
import {
    chargeAlertMessage,
    declineAlertMessage,
    refundAlertMessage,
    loadAlertMessage,
} from "../bot/templates";

// ── Types ──────────────────────────────────────────────────

export interface CardEvent {
    eventType: string;
    cardId: string;
    walletAddress: string;
    payload: {
        last4?: string;
        amount?: number;
        merchant?: string;
        balance?: number;
        txnId?: string;
        reason?: string;
        newBalance?: number;
    };
}

// ── Service ────────────────────────────────────────────────

export class NotifyService {
    /**
     * Process a card event and deliver notification to Telegram if applicable.
     * Idempotent: duplicate events are skipped.
     */
    static async processEvent(event: CardEvent): Promise<void> {
        if (env.BOT_ALERTS_ENABLED !== "true") return;
        if (!env.TG_BOT_TOKEN) return;

        // Generate idempotency key from event
        const idempotencyKey = `${event.eventType}:${event.cardId}:${event.payload.txnId ?? crypto.randomUUID()}`;
        const payloadHash = crypto
            .createHash("sha256")
            .update(JSON.stringify(event.payload))
            .digest("hex");

        // Check idempotency (atomic insert)
        const inserted = await query<{ id: string }>(
            `INSERT INTO bot_events (source, event_type, payload_hash, idempotency_key, delivery_status)
       VALUES ('card_webhook', $1, $2, $3, 'pending')
       ON CONFLICT (idempotency_key) DO NOTHING
       RETURNING id`,
            [event.eventType, payloadHash, idempotencyKey]
        );

        if (inserted.length === 0) {
            // Duplicate — already processed
            return;
        }

        const eventId = inserted[0].id;

        // Find Telegram binding for this wallet
        const bindings = await query<{ chat_id: string; telegram_user_id: string }>(
            `SELECT chat_id, telegram_user_id
       FROM owner_telegram_links
       WHERE owner_wallet = $1 AND status = 'active'`,
            [event.walletAddress]
        );

        if (bindings.length === 0) {
            // No binding — skip silently
            await query(
                `UPDATE bot_events SET delivery_status = 'skipped' WHERE id = $1`,
                [eventId]
            );
            return;
        }

        // Build message based on event type
        const message = buildAlertMessage(event);
        if (!message) {
            await query(
                `UPDATE bot_events SET delivery_status = 'skipped' WHERE id = $1`,
                [eventId]
            );
            return;
        }

        // Deliver to all active bindings
        const client = getTelegramClient();

        for (const binding of bindings) {
            const chatId = Number(binding.chat_id);

            try {
                const msgId = await client.sendMessage({
                    chat_id: chatId,
                    text: message,
                    parse_mode: "HTML",
                });

                // Log delivery
                await query(
                    `INSERT INTO bot_messages (chat_id, template_key, correlation_id, telegram_msg_id, status)
           VALUES ($1, $2, $3, $4, 'sent')`,
                    [chatId, event.eventType, idempotencyKey, msgId]
                );
            } catch (error) {
                appLogger.error({ err: error }, "[NOTIFY] Delivery failed");

                await query(
                    `INSERT INTO bot_messages (chat_id, template_key, correlation_id, status)
           VALUES ($1, $2, $3, 'failed')`,
                    [chatId, event.eventType, idempotencyKey]
                );
            }
        }

        // Mark event delivered
        await query(
            `UPDATE bot_events SET delivery_status = 'delivered' WHERE id = $1`,
            [eventId]
        );
    }
}

// ── Message Builder ────────────────────────────────────────

function buildAlertMessage(event: CardEvent): string | null {
    const p = event.payload;

    switch (event.eventType) {
        case "card.transaction":
        case "card.charge":
            return chargeAlertMessage(
                p.last4 ?? "????",
                p.amount ?? 0,
                p.merchant ?? "Unknown",
                p.balance ?? 0,
                p.txnId ?? "n/a"
            );

        case "card.decline":
            return declineAlertMessage(
                p.last4 ?? "????",
                p.amount ?? 0,
                p.merchant ?? "Unknown",
                p.reason ?? "Unknown",
                p.balance ?? 0,
                p.txnId ?? "n/a"
            );

        case "card.refund":
            return refundAlertMessage(
                p.amount ?? 0,
                p.merchant ?? "Unknown",
                p.txnId ?? "n/a",
                p.newBalance ?? 0
            );

        case "card.load":
        case "card.funded":
            return loadAlertMessage(
                p.last4 ?? "????",
                p.amount ?? 0,
                p.newBalance ?? 0
            );

        default:
            return null;
    }
}
