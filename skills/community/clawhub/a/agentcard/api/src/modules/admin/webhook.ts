/**
 * Admin Bot Webhook — handles Telegram updates for the admin bot.
 *
 * Minimal: only handles /start (to get chat_id) and /status.
 *
 * @module modules/admin/webhook
 */

import crypto from "node:crypto";
import { Router } from "express";
import { env } from "../../config/env";
import { TelegramClient } from "../bot/telegramClient";
import type { TgUpdate } from "../bot/telegramClient";
import { appLogger } from "../../utils/logger";
import { collectStatus, formatStatusMessage } from "./statusCollector";

export const adminRouter = Router();

let adminClient: TelegramClient | null = null;

function getClient(): TelegramClient {
    if (!adminClient) {
        if (!env.ADMIN_BOT_TOKEN) throw new Error("ADMIN_BOT_TOKEN required");
        adminClient = new TelegramClient(env.ADMIN_BOT_TOKEN);
    }
    return adminClient;
}

// ── Helpers ─────────────────────────────────────────────────

function safeEqual(a: string, b: string): boolean {
    const bufA = Buffer.from(a, "utf-8");
    const bufB = Buffer.from(b, "utf-8");
    if (bufA.length !== bufB.length) return false;
    return crypto.timingSafeEqual(bufA, bufB);
}

/** Derive admin webhook secret (must match what setup endpoint registers). */
function getAdminWebhookSecret(): string | null {
    return env.TG_WEBHOOK_SECRET ? `admin_${env.TG_WEBHOOK_SECRET}` : null;
}

// ── Webhook endpoint ───────────────────────────────────────

adminRouter.post("/telegram/webhook", async (req, res) => {
    // 1. Verify Telegram secret token (fail-closed)
    const expectedSecret = getAdminWebhookSecret();
    if (expectedSecret) {
        const headerToken = req.header("X-Telegram-Bot-Api-Secret-Token");
        if (!headerToken || !safeEqual(headerToken, expectedSecret)) {
            appLogger.warn(
                { ip: req.ip },
                "[AdminBot] Invalid webhook signature — rejecting"
            );
            res.status(401).json({ error: "Invalid webhook secret" });
            return;
        }
    }

    // 2. Parse update
    const update = req.body as TgUpdate;

    if (!update || !update.update_id) {
        res.status(400).json({ error: "Invalid update" });
        return;
    }

    try {
        const client = getClient();

        // ── Handle Callback Queries (button clicks) ──────────
        if (update.callback_query) {
            const cbq = update.callback_query;
            const cbChatId = cbq.message?.chat.id;
            if (!cbChatId || !cbq.data) {
                res.status(200).json({ ok: true });
                return;
            }

            // Acknowledge
            await client.answerCallbackQuery({ callback_query_id: cbq.id });

            if (cbq.data === "admin_status") {
                await client.sendMessage({
                    chat_id: cbChatId,
                    text: "⏳ Collecting status…",
                    parse_mode: "HTML",
                });
                const status = await collectStatus();
                const message = formatStatusMessage(status);
                await client.sendMessage({
                    chat_id: cbChatId,
                    text: message,
                    parse_mode: "HTML",
                    reply_markup: adminActionsKeyboard(),
                });
            } else if (cbq.data === "admin_help") {
                await sendHelpMessage(client, cbChatId);
            }

            res.status(200).json({ ok: true });
            return;
        }

        // ── Handle Text Messages (commands) ──────────────────
        const msg = update.message;

        if (msg?.text && msg.from) {
            const chatId = msg.chat.id;
            const text = msg.text.trim();

            if (text === "/start") {
                await client.sendMessage({
                    chat_id: chatId,
                    text:
                        `🛡️ <b>ASG Card Admin Bot</b>\n\n` +
                        `Your Chat ID: <code>${chatId}</code>\n\n` +
                        `Set this as <code>ADMIN_CHAT_ID</code> in your environment to receive notifications.\n\n` +
                        `<i>Only important events are pushed: transactions, errors, card operations.</i>`,
                    parse_mode: "HTML",
                    reply_markup: adminActionsKeyboard(),
                });
            } else if (text === "/status") {
                await client.sendMessage({
                    chat_id: chatId,
                    text: "⏳ Collecting status…",
                    parse_mode: "HTML",
                });

                const status = await collectStatus();
                const message = formatStatusMessage(status);

                await client.sendMessage({
                    chat_id: chatId,
                    text: message,
                    parse_mode: "HTML",
                    reply_markup: adminActionsKeyboard(),
                });
            } else if (text === "/help") {
                await sendHelpMessage(client, chatId);
            }
        }
    } catch (error) {
        appLogger.error({ err: error }, "[AdminBot] Update handling error");
    }

    res.status(200).json({ ok: true });
});

// ── Admin Keyboards ────────────────────────────────────────

function adminActionsKeyboard(): { inline_keyboard: { text: string; callback_data?: string; url?: string }[][] } {
    return {
        inline_keyboard: [
            [
                { text: "📊 Status", callback_data: "admin_status" },
                { text: "🔄 Refresh", callback_data: "admin_status" },
            ],
            [
                { text: "🌐 Dashboard", url: "https://asgcard.dev" },
                { text: "📖 API Docs", url: "https://docs.asgcard.dev" },
            ],
            [
                { text: "❓ Help", callback_data: "admin_help" },
            ],
        ],
    };
}

async function sendHelpMessage(client: TelegramClient, chatId: number): Promise<void> {
    await client.sendMessage({
        chat_id: chatId,
        text:
            `🛡️ <b>Admin Bot Commands</b>\n\n` +
            `/start — Setup info + Chat ID\n` +
            `/status — 📊 System status & metrics\n` +
            `/help — ❓ Show this message\n\n` +
            `<b>Auto-notifications:</b>\n` +
            `• 💳 Card operations (create, fund, freeze)\n` +
            `• 💰 Transactions (charges, declines, refunds)\n` +
            `• 🔗 Account linking events\n` +
            `• 🔴 Errors & webhook failures\n\n` +
            `<i>Or use the buttons below:</i>`,
        parse_mode: "HTML",
        reply_markup: adminActionsKeyboard(),
    });
}

// ── Setup endpoint (register webhook) ──────────────────────

adminRouter.post("/telegram/setup", async (req, res) => {
    const opsKey = env.OPS_API_KEY;
    if (!opsKey || req.header("X-Ops-Key") !== opsKey) {
        res.status(401).json({ error: "Unauthorized" });
        return;
    }

    try {
        const client = getClient();

        await client.setMyCommands([
            { command: "start", description: "Get chat ID & setup" },
            { command: "status", description: "📊 System status" },
            { command: "help", description: "Show commands" },
        ]);

        const baseUrl = process.env.API_BASE_URL ?? `https://${req.hostname}`;
        const webhookUrl = `${baseUrl}/admin/telegram/webhook`;
        // Generate admin webhook secret if not set
        const secret = env.TG_WEBHOOK_SECRET
            ? `admin_${env.TG_WEBHOOK_SECRET}`
            : crypto.randomUUID();

        await client.setWebhook(webhookUrl, secret, ["message", "callback_query"]);

        res.json({
            status: "ok",
            webhook: webhookUrl,
            commands: ["start", "status", "help"],
            note: "Send /start to the admin bot to get your ADMIN_CHAT_ID",
        });
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
});
