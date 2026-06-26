/**
 * Owner Policy — middleware that checks Telegram user binding.
 *
 * Extracts telegram_user_id from the TG update context,
 * looks up active binding in owner_telegram_links,
 * attaches ownerWallet to request or denies with audit.
 *
 * @module modules/authz/ownerPolicy
 */

import { query } from "../../db/db";
import { AuditService } from "./auditService";

// ── Types ──────────────────────────────────────────────────

export interface OwnerContext {
    ownerWallet: string;
    telegramUserId: number;
    chatId: number;
}

// ── Binding Lookup ─────────────────────────────────────────

/**
 * Look up active owner binding for a Telegram user.
 * Returns null if no active binding exists.
 */
export async function findActiveBinding(
    telegramUserId: number
): Promise<OwnerContext | null> {
    const rows = await query<{
        owner_wallet: string;
        telegram_user_id: string;
        chat_id: string;
    }>(
        `SELECT owner_wallet, telegram_user_id, chat_id
     FROM owner_telegram_links
     WHERE telegram_user_id = $1 AND status = 'active'
     LIMIT 1`,
        [telegramUserId]
    );

    if (rows.length === 0) return null;

    return {
        ownerWallet: rows[0].owner_wallet,
        telegramUserId: Number(rows[0].telegram_user_id),
        chatId: Number(rows[0].chat_id),
    };
}

/**
 * Middleware-style check: verify Telegram user has active binding.
 * Returns OwnerContext or null (with audit log on deny).
 */
export async function requireOwnerBinding(
    telegramUserId: number,
    action: string
): Promise<OwnerContext | null> {
    const binding = await findActiveBinding(telegramUserId);

    if (!binding) {
        await AuditService.log({
            actorType: "telegram_user",
            actorId: String(telegramUserId),
            action,
            decision: "deny",
            reason: "no_active_binding",
        });
        return null;
    }

    await AuditService.log({
        actorType: "telegram_user",
        actorId: String(telegramUserId),
        action,
        decision: "allow",
        reason: `bound_to_${binding.ownerWallet}`,
    });

    return binding;
}
