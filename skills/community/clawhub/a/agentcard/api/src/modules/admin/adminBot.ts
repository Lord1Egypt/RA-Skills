/**
 * Admin Bot — sends operational notifications to admin Telegram chat.
 *
 * A separate bot from @ASGCardbot. Receives all system events:
 * - 4payments webhook events (transactions, card issues, fees)
 * - Card creation & funding
 * - New account bindings
 * - Error alerts
 * - Bot command activity
 *
 * @module modules/admin
 */

import { TelegramClient } from "../bot/telegramClient";
import { env } from "../../config/env";
import { appLogger } from "../../utils/logger";

// ── Singleton ──────────────────────────────────────────────

let adminClient: TelegramClient | null = null;

function getAdminClient(): TelegramClient | null {
    if (env.ADMIN_BOT_ENABLED !== "true" || !env.ADMIN_BOT_TOKEN) return null;
    if (!adminClient) {
        adminClient = new TelegramClient(env.ADMIN_BOT_TOKEN);
    }
    return adminClient;
}

function getAdminChatIds(): number[] {
    if (!env.ADMIN_CHAT_ID) return [];
    return env.ADMIN_CHAT_ID.split(",").map((id) => Number(id.trim())).filter((id) => !isNaN(id) && id !== 0);
}

// ── Public API ─────────────────────────────────────────────

export const AdminBot = {
    /**
     * Send a raw message to the admin chat.
     * Safe to call even if admin bot is disabled — silently skips.
     */
    async send(text: string, parseMode: "HTML" | "Markdown" = "HTML"): Promise<void> {
        const client = getAdminClient();
        const chatIds = getAdminChatIds();
        if (!client || chatIds.length === 0) return;

        for (const chatId of chatIds) {
            try {
                await client.sendMessage({
                    chat_id: chatId,
                    text,
                    parse_mode: parseMode,
                });
            } catch (err) {
                appLogger.error({ err, chatId }, "[AdminBot] Failed to send message");
            }
        }
    },

    // ── Card Events ────────────────────────────────────────

    async cardCreated(data: {
        cardId: string;
        wallet: string;
        tier: number;
        balance: number;
        last4: string;
    }): Promise<void> {
        await this.send(
            `🆕 <b>Card Created</b>\n` +
            `├ Card: <code>xxxx ${data.last4}</code>\n` +
            `├ Tier: $${data.tier}\n` +
            `├ Balance: $${data.balance.toFixed(2)}\n` +
            `├ Wallet: <code>${data.wallet.slice(0, 8)}…${data.wallet.slice(-4)}</code>\n` +
            `└ ID: <code>${data.cardId.slice(0, 8)}</code>`
        );
    },

    async cardFunded(data: {
        cardId: string;
        amount: number;
        newBalance: number;
        last4: string;
        txHash: string;
    }): Promise<void> {
        await this.send(
            `💰 <b>Card Funded</b>\n` +
            `├ Card: <code>xxxx ${data.last4}</code>\n` +
            `├ Amount: +$${data.amount.toFixed(2)}\n` +
            `├ New Balance: $${data.newBalance.toFixed(2)}\n` +
            `└ TX: <code>${data.txHash.slice(0, 12)}…</code>`
        );
    },

    async cardFrozen(cardId: string, last4: string, by: string): Promise<void> {
        await this.send(
            `❄️ <b>Card Frozen</b>\n` +
            `├ Card: <code>xxxx ${last4}</code>\n` +
            `├ By: <code>${by}</code>\n` +
            `└ ID: <code>${cardId.slice(0, 8)}</code>`
        );
    },

    async cardUnfrozen(cardId: string, last4: string, by: string): Promise<void> {
        await this.send(
            `🔥 <b>Card Unfrozen</b>\n` +
            `├ Card: <code>xxxx ${last4}</code>\n` +
            `├ By: <code>${by}</code>\n` +
            `└ ID: <code>${cardId.slice(0, 8)}</code>`
        );
    },

    // ── Webhook Events (from 4payments) ────────────────────

    async webhookReceived(data: {
        type: string;
        idempotencyKey: string;
        payload: Record<string, unknown>;
    }): Promise<void> {
        const summary = JSON.stringify(data.payload, null, 0).slice(0, 200);
        await this.send(
            `📨 <b>4P Webhook</b>: <code>${data.type}</code>\n` +
            `├ Key: <code>${data.idempotencyKey.slice(0, 16)}</code>\n` +
            `└ <pre>${escapeHtml(summary)}</pre>`
        );
    },

    async webhookDuplicate(_type: string, _key: string): Promise<void> {
        // Silently skip — duplicates are normal idempotency (not worth admin noise)
    },

    async webhookSigFailure(ip: string): Promise<void> {
        await this.send(
            `🚫 <b>Webhook Signature Failed</b>\n` +
            `└ IP: <code>${ip}</code>`
        );
    },

    // ── Account Linking ────────────────────────────────────

    async accountLinked(data: {
        wallet: string;
        telegramUserId: number;
        username?: string;
    }): Promise<void> {
        const user = data.username ? `@${data.username}` : `ID:${data.telegramUserId}`;
        await this.send(
            `🔗 <b>Account Linked</b>\n` +
            `├ TG: ${escapeHtml(user)}\n` +
            `└ Wallet: <code>${data.wallet.slice(0, 8)}…${data.wallet.slice(-4)}</code>`
        );
    },

    // ── Transaction Alerts (mirror) ────────────────────────

    async transaction(data: {
        type: string;
        last4: string;
        amount: number;
        merchant?: string;
        balance?: number;
        reason?: string;
    }): Promise<void> {
        const icon = data.type.includes("decline") ? "❌" :
                     data.type.includes("refund") ? "↩️" :
                     data.type.includes("fee") ? "💸" : "💳";
        await this.send(
            `${icon} <b>Transaction</b>: ${escapeHtml(data.type)}\n` +
            `├ Card: xxxx ${data.last4}\n` +
            `├ Amount: $${data.amount.toFixed(2)}\n` +
            (data.merchant ? `├ Merchant: ${escapeHtml(data.merchant)}\n` : "") +
            (data.balance != null ? `├ Balance: $${data.balance.toFixed(2)}\n` : "") +
            (data.reason ? `├ Reason: ${escapeHtml(data.reason)}\n` : "") +
            `└ Type: <code>${data.type}</code>`
        );
    },

    // ── Bot Commands ───────────────────────────────────────

    async botCommand(userId: number, command: string, username?: string): Promise<void> {
        // Only log financially-relevant commands, skip routine ones
        const routineCommands = ["/start", "/mycards", "/help", "/faq"];
        const cmd = command.split(" ")[0].toLowerCase();
        if (routineCommands.includes(cmd)) return;

        const user = username ? `@${username}` : `ID:${userId}`;
        await this.send(
            `🤖 <b>Bot Command</b>\n` +
            `├ User: ${escapeHtml(user)}\n` +
            `└ Cmd: <code>${escapeHtml(command)}</code>`
        );
    },

    async rateLimited(userId: number): Promise<void> {
        await this.send(
            `⚠️ <b>Rate Limited</b>\n` +
            `└ User ID: <code>${userId}</code>`
        );
    },

    // ── Errors ─────────────────────────────────────────────

    async error(context: string, error: Error | string): Promise<void> {
        const msg = typeof error === "string" ? error : error.message;
        await this.send(
            `🔴 <b>Error</b>: ${escapeHtml(context)}\n` +
            `└ <pre>${escapeHtml(msg.slice(0, 500))}</pre>`
        );
    },

    // ── System ─────────────────────────────────────────────

    // startup() removed — fires on every Vercel cold start, creating spam
    // deploy() removed — not called from anywhere

    /** Expose the underlying TelegramClient for advanced usage (e.g. admin webhook) */
    getClient: getAdminClient,
    getChatIds: getAdminChatIds,
};

// ── Helpers ────────────────────────────────────────────────

import { escapeHtml } from "../../utils/html";
