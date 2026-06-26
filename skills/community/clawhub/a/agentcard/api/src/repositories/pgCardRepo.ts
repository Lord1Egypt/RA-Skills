import crypto from "node:crypto";
import { query, getPool } from "../db/db";
import type { StoredCard, CardDetails } from "../types/domain";
import type { CardRepository, CreateCardInput } from "./types";
import { encryptCardDetails, decryptCardDetails, parseEncryptionKey } from "../utils/crypto";

/**
 * Postgres-backed card repository.
 * Card details are encrypted at rest with AES-256-GCM.
 * NUMERIC columns are explicitly cast to number via parseFloat.
 */
export class PostgresCardRepository implements CardRepository {
    private readonly encKey: Buffer;

    constructor() {
        const keyEnv = process.env.CARD_DETAILS_KEY;
        if (!keyEnv) {
            throw new Error("CARD_DETAILS_KEY is required when REPO_MODE=postgres");
        }
        this.encKey = parseEncryptionKey(keyEnv);
    }

    async create(input: CreateCardInput): Promise<StoredCard> {
        const cardId = `card_${crypto.randomUUID().slice(0, 8)}`;
        const detailsEncrypted = encryptCardDetails(input.details, this.encKey);

        // Extract last4 from card details
        const last4 = input.details.maskedCardNumber
            ? (input.details.maskedCardNumber.replace(/[^0-9]/g, '').slice(-4) || null)
            : (input.details.cardNumber ? input.details.cardNumber.slice(-4) : null);

        const rows = await query<CardRow>(
            `INSERT INTO cards
               (card_id, wallet_address, name_on_card, email, balance, initial_amount, status, details_encrypted, details_revoked, four_payments_id, last_four)
             VALUES ($1, $2, $3, $4, $5, $6, 'active', $7, false, $8, $9)
             RETURNING card_id, wallet_address, name_on_card, email,
                       balance, initial_amount, status, details_encrypted, details_revoked, four_payments_id, last_four,
                       created_at, updated_at`,
            [
                cardId,
                input.walletAddress,
                input.nameOnCard,
                input.email,
                input.initialAmountUsd,
                input.initialAmountUsd,
                detailsEncrypted,
                input.fourPaymentsId || null,
                last4
            ]
        );

        return this.rowToStoredCard(rows[0]);
    }

    async findById(cardId: string): Promise<StoredCard | undefined> {
        const rows = await query<CardRow>(
            `SELECT card_id, wallet_address, name_on_card, email,
                    balance, initial_amount, status, details_encrypted, details_revoked, four_payments_id, last_four,
                    created_at, updated_at
             FROM cards
             WHERE card_id = $1`,
            [cardId]
        );

        return rows.length > 0 ? this.rowToStoredCard(rows[0]) : undefined;
    }

    async findByWallet(walletAddress: string): Promise<StoredCard[]> {
        const rows = await query<CardRow>(
            `SELECT card_id, wallet_address, name_on_card, email,
                    balance, initial_amount, status, details_encrypted, details_revoked, four_payments_id, last_four,
                    created_at, updated_at
             FROM cards
             WHERE wallet_address = $1
             ORDER BY created_at DESC`,
            [walletAddress]
        );

        return rows.map((r) => this.rowToStoredCard(r));
    }

    async updateStatus(
        cardId: string,
        status: "active" | "frozen"
    ): Promise<boolean> {
        const rows = await query(
            `UPDATE cards SET status = $2 WHERE card_id = $1 RETURNING card_id`,
            [cardId, status]
        );
        return rows.length > 0;
    }

    async addBalance(cardId: string, amount: number): Promise<boolean> {
        const rows = await query(
            `UPDATE cards SET balance = balance + $2 WHERE card_id = $1 RETURNING card_id`,
            [cardId, amount]
        );
        return rows.length > 0;
    }

    // REALIGN-005: Owner can revoke agent access to card details
    async setDetailsRevoked(cardId: string, revoked: boolean): Promise<boolean> {
        const rows = await query(
            `UPDATE cards SET details_revoked = $2 WHERE card_id = $1 RETURNING card_id`,
            [cardId, revoked]
        );
        return rows.length > 0;
    }

    // REALIGN-003: Atomic Nonce & Rate Limit check
    async recordNonceAndCheckRateLimit(walletAddress: string, cardId: string, nonce: string, limitPerHour: number): Promise<{
        allowed: boolean;
        reason?: 'replay' | 'rate_limit';
        retryAfterSeconds?: number;
    }> {
        const pool = getPool();
        const client = await pool.connect();

        try {
            await client.query('BEGIN');
            // Acquire advisory lock serialized on cardId hash
            await client.query('SELECT pg_advisory_xact_lock(hashtext($1))', [cardId]);

            const result = await client.query<{
                current_count: string;
                inserted_nonce: string | null;
                existing_nonce: string | null;
            }>(`
                WITH count_reads AS (
                   SELECT count(*) as cnt FROM agent_nonces WHERE card_id = $1 AND created_at >= NOW() - INTERVAL '1 hour'
                ),
                nonce_check AS (
                   SELECT nonce FROM agent_nonces WHERE nonce = $2
                ),
                insert_nonce AS (
                   INSERT INTO agent_nonces (nonce, wallet, card_id)
                   SELECT $2, $3, $1
                   FROM count_reads
                   WHERE cnt < $4 AND NOT EXISTS (SELECT 1 FROM nonce_check)
                   ON CONFLICT (nonce) DO NOTHING
                   RETURNING nonce
                )
                SELECT 
                   (SELECT cnt FROM count_reads) as current_count,
                   (SELECT nonce FROM insert_nonce) as inserted_nonce,
                   (SELECT nonce FROM nonce_check) as existing_nonce
            `, [cardId, nonce, walletAddress, limitPerHour]);

            await client.query('COMMIT');

            const row = result.rows[0];
            if (row.inserted_nonce) {
                return { allowed: true };
            }
            if (row.existing_nonce) {
                return { allowed: false, reason: 'replay' };
            }
            const count = parseInt(row.current_count, 10);
            if (count >= limitPerHour) {
                return { allowed: false, reason: 'rate_limit', retryAfterSeconds: 3600 };
            }
            return { allowed: false, reason: 'replay' };
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        } finally {
            client.release();
        }
    }

    // ── Row mapping ─────────────────────────────────────────

    private rowToStoredCard(row: CardRow): StoredCard {
        let details: CardDetails;
        try {
            details = decryptCardDetails(row.details_encrypted, this.encKey);
        } catch {
            // Decryption may fail for cards without details_encrypted
            details = {
                cardNumber: "",
                expiryMonth: 0,
                expiryYear: 0,
                cvv: "",
                billingAddress: { street: "", city: "", state: "", zip: "", country: "" },
            };
        }
        return {
            cardId: row.card_id,
            walletAddress: row.wallet_address,
            nameOnCard: row.name_on_card,
            email: row.email,
            balance: parseFloat(row.balance),
            initialAmountUsd: parseFloat(row.initial_amount),
            status: row.status as "active" | "frozen",
            createdAt: row.created_at.toISOString(),
            updatedAt: row.updated_at.toISOString(),
            details,
            fourPaymentsId: row.four_payments_id || undefined,
            detailsRevoked: row.details_revoked,
            lastFour: row.last_four || undefined,
        } as StoredCard & { detailsRevoked: boolean; lastFour?: string };
    }
}

// ── Shared row type ────────────────────────────────────────
interface CardRow {
    card_id: string;
    wallet_address: string;
    name_on_card: string;
    email: string;
    balance: string;
    initial_amount: string;
    status: string;
    details_encrypted: Buffer;
    details_revoked: boolean;
    four_payments_id: string | null;
    last_four: string | null;
    created_at: Date;
    updated_at: Date;
}
