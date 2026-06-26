import { query } from "../db/db";
import type { PaymentRecord, PaymentRepository, PaymentStatus } from "./types";
import type { TierAmount } from "../types/domain";

/**
 * Postgres-backed payment repository.
 *
 * Anti-replay is atomic: INSERT ... ON CONFLICT (tx_hash) DO NOTHING.
 * If the insert returns 0 rows, the txHash was already used.
 */
export class PostgresPaymentRepository implements PaymentRepository {
    async recordPayment(
        payment: Omit<PaymentRecord, "id" | "createdAt" | "updatedAt">
    ): Promise<{ record: PaymentRecord; inserted: boolean }> {
        const rows = await query<{
            id: string;
            tx_hash: string;
            payer: string;
            amount: string;
            tier_amount: number;
            status: string;
            settle_id: string | null;
            card_id: string | null;
            created_at: Date;
            updated_at: Date;
        }>(
            `INSERT INTO payments (tx_hash, payer, amount, tier_amount, status, settle_id, card_id)
             VALUES ($1, $2, $3, $4, $5, $6, $7)
             ON CONFLICT (tx_hash) DO NOTHING
             RETURNING id, tx_hash, payer, amount, tier_amount, status,
                       settle_id, card_id, created_at, updated_at`,
            [
                payment.txHash,
                payment.payer,
                payment.amount,
                payment.tierAmount,
                payment.status,
                payment.settleId ?? null,
                payment.cardId ?? null
            ]
        );

        // ON CONFLICT → 0 rows means duplicate txHash (anti-replay)
        if (rows.length === 0) {
            const existing = await this.findByTxHash(payment.txHash);
            if (existing) return { record: existing, inserted: false };
            throw new Error(`Payment conflict for tx_hash=${payment.txHash} but record not found`);
        }

        return { record: this.rowToPaymentRecord(rows[0]), inserted: true };
    }

    async findByTxHash(txHash: string): Promise<PaymentRecord | undefined> {
        const rows = await query<{
            id: string;
            tx_hash: string;
            payer: string;
            amount: string;
            tier_amount: number;
            status: string;
            settle_id: string | null;
            card_id: string | null;
            created_at: Date;
            updated_at: Date;
        }>(
            `SELECT id, tx_hash, payer, amount, tier_amount, status,
                    settle_id, card_id, created_at, updated_at
             FROM payments
             WHERE tx_hash = $1`,
            [txHash]
        );

        return rows.length > 0 ? this.rowToPaymentRecord(rows[0]) : undefined;
    }

    async markSettled(txHash: string, settleId: string): Promise<boolean> {
        const rows = await query(
            `UPDATE payments
             SET status = 'settled', settle_id = $2
             WHERE tx_hash = $1
             RETURNING id`,
            [txHash, settleId]
        );
        return rows.length > 0;
    }

    async markFailed(
        txHash: string,
        status: "settle_failed" | "verify_failed"
    ): Promise<boolean> {
        const rows = await query(
            `UPDATE payments SET status = $2 WHERE tx_hash = $1 RETURNING id`,
            [txHash, status]
        );
        return rows.length > 0;
    }

    // ── Row mapping ─────────────────────────────────────────

    private rowToPaymentRecord(row: {
        id: string;
        tx_hash: string;
        payer: string;
        amount: string;
        tier_amount: number;
        status: string;
        settle_id: string | null;
        card_id: string | null;
        created_at: Date;
        updated_at: Date;
    }): PaymentRecord {
        return {
            id: row.id,
            txHash: row.tx_hash,
            payer: row.payer,
            amount: row.amount,
            tierAmount: row.tier_amount as TierAmount,
            status: row.status as PaymentStatus,
            settleId: row.settle_id ?? undefined,
            cardId: row.card_id ?? undefined,
            createdAt: row.created_at.toISOString(),
            updatedAt: row.updated_at.toISOString()
        };
    }
}
