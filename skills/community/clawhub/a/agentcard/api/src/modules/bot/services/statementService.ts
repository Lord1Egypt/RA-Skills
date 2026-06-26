/**
 * Statement Service — queries real transaction history from bot_events + webhook_events.
 *
 * Supports pagination, status mapping: pending/declined/settled/reversed.
 *
 * @module modules/bot/services/statementService
 */

import { query } from "../../../db/db";

// ── Types ──────────────────────────────────────────────────

export type TransactionStatus = "pending" | "declined" | "settled" | "reversed";

export interface StatementEntry {
    txnId: string;
    date: string;
    type: string;
    merchant: string;
    amount: number;
    status: TransactionStatus;
    last4: string;
}

export interface StatementPage {
    items: StatementEntry[];
    total: number;
    page: number;
    pageSize: number;
    hasMore: boolean;
}

// ── Event-Type → Status Mapping ────────────────────────────

const EVENT_STATUS_MAP: Record<string, TransactionStatus> = {
    "card.transaction": "settled",
    "card.charge": "settled",
    "card.authorization": "pending",
    "card.authorized": "pending",
    "card.decline": "declined",
    "card.refund": "reversed",
    "card.reversal": "reversed",
    "card.load": "settled",
    "card.funded": "settled",
};

function mapEventStatus(eventType: string): TransactionStatus {
    return EVENT_STATUS_MAP[eventType] ?? "pending";
}

// ── Service ────────────────────────────────────────────────

export class StatementService {
    /**
     * Retrieve statement for a specific card, with pagination.
     * Pulls from bot_events table (which tracks all card events).
     */
    static async getStatement(
        walletAddress: string,
        cardId: string,
        page = 1,
        pageSize = 10
    ): Promise<StatementPage> {
        const offset = (page - 1) * pageSize;

        // Escape SQL LIKE special chars to prevent pattern injection (P0 #3)
        const safeCardId = cardId.replace(/[%_\\]/g, "\\$&");

        // Count total events for this card
        const countResult = await query<{ count: string }>(
            `SELECT COUNT(*) as count
       FROM bot_events be
       WHERE be.idempotency_key LIKE $1
         AND be.delivery_status != 'skipped'`,
            [`%:${safeCardId}:%`]
        );

        const total = parseInt(countResult[0]?.count ?? "0", 10);

        // Fetch paginated events with merchant/amount via LEFT JOIN (no N+1)
        const rows = await query<{
            idempotency_key: string;
            event_type: string;
            payload_hash: string;
            created_at: string;
            merchant: string;
            amount: number;
            card_last4: string;
        }>(
            `SELECT
               be.idempotency_key,
               be.event_type,
               be.payload_hash,
               be.created_at,
               COALESCE(
                 we.payload->>'merchant',
                 we.payload->>'merchant_name',
                 'Unknown'
               ) as merchant,
               COALESCE(
                 (we.payload->>'amount')::numeric,
                 (we.payload->>'transaction_amount')::numeric,
                 0
               ) as amount,
               COALESCE(
                 we.payload->>'card_last4',
                 RIGHT(we.payload->>'card_number', 4),
                 '????'
               ) as card_last4
             FROM bot_events be
             LEFT JOIN webhook_events we
               ON we.event_type = be.event_type
              AND we.idempotency_key = be.idempotency_key
             WHERE be.idempotency_key LIKE $1
               AND be.delivery_status != 'skipped'
             ORDER BY be.created_at DESC
             LIMIT $2 OFFSET $3`,
            [`%:${safeCardId}:%`, pageSize, offset]
        );

        // Build statement entries
        const items: StatementEntry[] = rows.map((row) => {
            const parts = row.idempotency_key.split(":");
            const txnId = parts[2] ?? row.payload_hash.substring(0, 12);

            return {
                txnId,
                date: row.created_at,
                type: row.event_type.replace("card.", ""),
                merchant: row.merchant,
                amount: Number(row.amount),
                status: mapEventStatus(row.event_type),
                last4: row.card_last4,
            };
        });

        return {
            items,
            total,
            page,
            pageSize,
            hasMore: offset + pageSize < total,
        };
    }

    /**
     * Format statement page as Telegram HTML message.
     */
    static formatStatementMessage(
        last4: string,
        statement: StatementPage
    ): string {
        if (statement.items.length === 0) {
            return (
                `📊 <b>Statement</b> — Card xxxx ${last4}\n\n` +
                `No transactions found.\n\n` +
                `<i>Page ${statement.page} of ${Math.max(1, Math.ceil(statement.total / statement.pageSize))}</i>`
            );
        }

        const statusIcon: Record<TransactionStatus, string> = {
            settled: "✅",
            pending: "⏳",
            declined: "❌",
            reversed: "↩️",
        };

        const lines = statement.items.map((item) => {
            const icon = statusIcon[item.status] ?? "❔";
            const date = new Date(item.date).toLocaleDateString("en-US", {
                month: "short",
                day: "numeric",
            });
            const sign = ["reversed", "declined"].includes(item.status) ? "" : "-";
            return `${icon} ${date} │ ${sign}$${item.amount.toFixed(2)} │ ${item.merchant}\n   <i>${item.status}</i> • <code>${item.txnId.substring(0, 10)}</code>`;
        });

        const totalPages = Math.max(1, Math.ceil(statement.total / statement.pageSize));

        return (
            `📊 <b>Statement</b> — Card xxxx ${last4}\n\n` +
            lines.join("\n\n") +
            `\n\n<i>Page ${statement.page}/${totalPages} (${statement.total} total)</i>`
        );
    }
}
