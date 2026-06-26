/**
 * Link Service — issue, consume, and revoke Telegram link tokens.
 *
 * BOT-102 model:
 * 1. Owner logs into portal with wallet
 * 2. Portal calls issueToken → gets deep-link URL
 * 3. Owner clicks deep-link → Telegram sends /start lnk_<token>
 * 4. Bot calls consumeToken → atomic bind
 *
 * Tokens are stored hashed (SHA-256), single-use, TTL 10 minutes.
 *
 * @module modules/portal/linkService
 */

import crypto from "node:crypto";
import { query } from "../../db/db";
import { AuditService } from "../authz/auditService";

// ── Constants ──────────────────────────────────────────────

const TOKEN_TTL_MS = 10 * 60 * 1000; // 10 minutes
const TOKEN_PREFIX = "lnk_";
const BOT_USERNAME = process.env.TG_BOT_USERNAME ?? "ASGCardbot";

// ── Types ──────────────────────────────────────────────────

export interface IssuedToken {
    deepLink: string;
    expiresAt: string;
}

export interface ConsumeResult {
    success: boolean;
    ownerWallet?: string;
    error?: string;
}

// ── Helpers ────────────────────────────────────────────────

function hashToken(raw: string): string {
    return crypto.createHash("sha256").update(raw).digest("hex");
}

function generateToken(): string {
    return TOKEN_PREFIX + crypto.randomBytes(24).toString("base64url");
}

// ── Service ────────────────────────────────────────────────

export class LinkService {
    /**
     * Issue a one-time capability token for Telegram linking.
     * Called from portal when owner clicks "Connect Telegram".
     */
    static async issueToken(ownerWallet: string, ip?: string): Promise<IssuedToken> {
        // Revoke any existing pending tokens for this wallet
        await query(
            `UPDATE telegram_link_tokens
       SET status = 'revoked'
       WHERE owner_wallet = $1 AND status = 'pending'`,
            [ownerWallet]
        );

        const raw = generateToken();
        const hash = hashToken(raw);
        const expiresAt = new Date(Date.now() + TOKEN_TTL_MS);

        await query(
            `INSERT INTO telegram_link_tokens
         (token_hash, owner_wallet, scope, expires_at, created_by_ip, status)
       VALUES ($1, $2, 'telegram_link', $3, $4, 'pending')`,
            [hash, ownerWallet, expiresAt.toISOString(), ip ?? null]
        );

        await AuditService.log({
            actorType: "wallet_owner",
            actorId: ownerWallet,
            action: "link_token_issued",
            decision: "allow",
            ipAddress: ip,
        });

        return {
            deepLink: `https://t.me/${BOT_USERNAME}?start=${raw}`,
            expiresAt: expiresAt.toISOString(),
        };
    }

    /**
     * Consume a link token and create binding.
     * Called from bot /start handler.
     *
     * Atomic: verify hash → check TTL → check single-use → create binding.
     * Deny conditions: expired, already consumed, invalid hash.
     */
    static async consumeToken(
        rawToken: string,
        telegramUserId: number,
        chatId: number
    ): Promise<ConsumeResult> {
        const hash = hashToken(rawToken);

        // Atomic consume: UPDATE ... WHERE status = 'pending' AND expires_at > now()
        const consumed = await query<{ owner_wallet: string }>(
            `UPDATE telegram_link_tokens
       SET status = 'consumed', consumed_at = now()
       WHERE token_hash = $1
         AND status = 'pending'
         AND expires_at > now()
       RETURNING owner_wallet`,
            [hash]
        );

        if (consumed.length === 0) {
            // Check why it failed for audit purposes
            const existing = await query<{ status: string; expires_at: string }>(
                `SELECT status, expires_at FROM telegram_link_tokens WHERE token_hash = $1`,
                [hash]
            );

            let reason = "invalid_token";
            if (existing.length > 0) {
                const row = existing[0];
                if (row.status === "consumed") reason = "token_already_consumed";
                else if (new Date(row.expires_at) <= new Date()) reason = "token_expired";
                else if (row.status === "revoked") reason = "token_revoked";
            }

            await AuditService.log({
                actorType: "telegram_user",
                actorId: String(telegramUserId),
                action: "link_token_consume_attempt",
                decision: "deny",
                reason,
            });

            return { success: false, error: reason };
        }

        const ownerWallet = consumed[0].owner_wallet;

        // Upsert binding (re-link if previously revoked)
        await query(
            `INSERT INTO owner_telegram_links
         (owner_wallet, telegram_user_id, chat_id, status)
       VALUES ($1, $2, $3, 'active')
       ON CONFLICT (owner_wallet, telegram_user_id)
       DO UPDATE SET
         chat_id = EXCLUDED.chat_id,
         status = 'active',
         linked_at = now(),
         revoked_at = NULL`,
            [ownerWallet, telegramUserId, chatId]
        );

        await AuditService.log({
            actorType: "telegram_user",
            actorId: String(telegramUserId),
            action: "telegram_linked",
            resourceId: ownerWallet,
            decision: "allow",
        });

        return { success: true, ownerWallet };
    }

    /**
     * Revoke Telegram binding for a wallet.
     * Called from portal when owner clicks "Disconnect Telegram".
     * Immediately invalidates bot access.
     */
    static async revokeBinding(ownerWallet: string, ip?: string): Promise<boolean> {
        const result = await query<{ id: string }>(
            `UPDATE owner_telegram_links
       SET status = 'revoked', revoked_at = now()
       WHERE owner_wallet = $1 AND status = 'active'
       RETURNING id`,
            [ownerWallet]
        );

        await AuditService.log({
            actorType: "wallet_owner",
            actorId: ownerWallet,
            action: "telegram_revoked",
            decision: "allow",
            reason: result.length > 0 ? "binding_revoked" : "no_active_binding",
            ipAddress: ip,
        });

        return result.length > 0;
    }

    /**
     * Get link status for a wallet.
     */
    static async getStatus(ownerWallet: string): Promise<{
        linked: boolean;
        telegramUserId?: number;
        linkedAt?: string;
    }> {
        const rows = await query<{
            telegram_user_id: string;
            linked_at: string;
        }>(
            `SELECT telegram_user_id, linked_at
       FROM owner_telegram_links
       WHERE owner_wallet = $1 AND status = 'active'
       LIMIT 1`,
            [ownerWallet]
        );

        if (rows.length === 0) return { linked: false };

        return {
            linked: true,
            telegramUserId: Number(rows[0].telegram_user_id),
            linkedAt: rows[0].linked_at,
        };
    }
}
