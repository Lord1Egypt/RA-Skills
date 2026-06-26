import { appLogger } from "../../utils/logger";
/**
 * Bot Webhook — Telegram update handler.
 *
 * POST /bot/telegram/webhook
 *
 * Verifies X-Telegram-Bot-Api-Secret-Token, parses update,
 * routes to command handlers. Fail-closed on invalid signatures.
 *
 * @module modules/bot/webhook
 */

import crypto from "node:crypto";
import { Router } from "express";
import { env } from "../../config/env";
import { TelegramClient } from "./telegramClient";
import type { TgUpdate, TgMessage, TgCallbackQuery } from "./telegramClient";
import { handleStartCommand } from "./commands/start";
import { handleMyCardsCommand, handleCardCallback } from "./commands/myCards";
import { handleProfileCommand, handleProfileCallback, handleProfileInput } from "./commands/profile";
import { handleFaqCommand } from "./commands/faq";
import { handleSupportCommand } from "./commands/support";
import { handleFundCommand, handleFundCallback } from "./commands/fund";
import { AuditService } from "../authz/auditService";
import { AdminBot } from "../admin/adminBot";

// ── Router ─────────────────────────────────────────────────

export const botRouter = Router();

/** Lazily initialized Telegram client (only when bot is enabled). */
let tgClient: TelegramClient | null = null;

export function getTelegramClient(): TelegramClient {
    if (!tgClient) {
        if (!env.TG_BOT_TOKEN) {
            throw new Error("TG_BOT_TOKEN is required when TG_BOT_ENABLED=true");
        }
        tgClient = new TelegramClient(env.TG_BOT_TOKEN);
    }
    return tgClient;
}

// ── Rate Limiter (per-instance, fits serverless warm instances) ──
// Note: On Vercel serverless each cold start resets state.
// For cross-instance rate limiting, use Redis/KV in a future phase.
const rateLimitMap = new Map<number, { count: number; resetAt: number }>();
const RATE_LIMIT_WINDOW_MS = 60_000; // 1 minute
const RATE_LIMIT_MAX = 30; // 30 actions per minute per user
const RATE_LIMIT_MAX_ENTRIES = 10_000; // safety cap
let lastCleanup = Date.now();

function checkRateLimit(userId: number): boolean {
    const now = Date.now();

    // Periodic cleanup: purge expired entries every 5 min (or if Map is too big)
    if (now - lastCleanup > 5 * 60_000 || rateLimitMap.size > RATE_LIMIT_MAX_ENTRIES) {
        for (const [key, val] of rateLimitMap) {
            if (now > val.resetAt) rateLimitMap.delete(key);
        }
        lastCleanup = now;
    }

    const entry = rateLimitMap.get(userId);
    if (!entry || now > entry.resetAt) {
        rateLimitMap.set(userId, { count: 1, resetAt: now + RATE_LIMIT_WINDOW_MS });
        return true;
    }
    entry.count++;
    if (entry.count > RATE_LIMIT_MAX) return false;
    return true;
}

/** Strip @botusername from commands (P2 #11) */
/** Basic card ID format validation (alphanumeric + underscores, 5-64 chars) */
function isValidCardId(id: string): boolean {
    return /^[a-zA-Z0-9_-]{5,64}$/.test(id);
}

function normalizeCommand(text: string): string {
    return text.replace(/@\S+/, "").trim();
}

// ── Webhook endpoint ───────────────────────────────────────

botRouter.post("/telegram/webhook", async (req, res) => {
    // 1. Verify Telegram secret token (fail-closed)
    if (env.TG_WEBHOOK_SECRET) {
        const headerToken = req.header("X-Telegram-Bot-Api-Secret-Token");
        if (!headerToken || !safeEqual(headerToken, env.TG_WEBHOOK_SECRET)) {
            await AuditService.log({
                actorType: "system",
                actorId: "telegram_webhook",
                action: "webhook_signature_invalid",
                decision: "deny",
                ipAddress: req.ip,
            });
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

    // 3. Process update BEFORE responding (Vercel kills function after res.send)
    try {
        const client = getTelegramClient();

        if (update.message) {
            const userId = update.message.from?.id;
            if (userId && !checkRateLimit(userId)) {
                AdminBot.rateLimited(userId).catch(() => {});
                res.status(200).json({ ok: true });
                return;
            }
            await handleMessage(client, update.message);
        } else if (update.callback_query) {
            const userId = update.callback_query.from?.id;
            if (userId && !checkRateLimit(userId)) {
                await client.answerCallbackQuery({
                    callback_query_id: update.callback_query.id,
                    text: "Too many requests. Please wait a moment.",
                    show_alert: true,
                });
                res.status(200).json({ ok: true });
                return;
            }
            await handleCallback(client, update.callback_query);
        }
    } catch (error) {
        appLogger.error({ err: error }, "[BOT] Update handling error");
    }

    // 4. Respond 200 after processing (Telegram retries on non-200)
    res.status(200).json({ ok: true });
});
// ── Webhook Health (P3) ────────────────────────────────────

botRouter.get("/telegram/health", async (_req, res) => {
    try {
        const client = getTelegramClient();
        const info = await client.getWebhookInfo();
        res.json({
            status: info.url ? "active" : "not_set",
            url: info.url,
            pending_update_count: info.pending_update_count,
            last_error_date: info.last_error_date,
            last_error_message: info.last_error_message,
        });
    } catch (error) {
        res.status(500).json({ status: "error", message: (error as Error).message });
    }
});

// ── Setup command (one-time, called manually or on deploy) ──

botRouter.post("/telegram/setup", async (req, res) => {
    // Protected: require ops key (P3 #14: fail-closed)
    const opsKey = env.OPS_API_KEY;
    if (!opsKey || req.header("X-Ops-Key") !== opsKey) {
        res.status(401).json({ error: "Unauthorized" });
        return;
    }

    try {
        const client = getTelegramClient();

        // Set persistent menu commands
        await client.setMyCommands([
            { command: "start", description: "Start / Link account" },
            { command: "mycards", description: "💳 My Cards" },
            { command: "profile", description: "👤 Profile" },
            { command: "fund", description: "💰 Fund a Card" },
            { command: "faq", description: "❓ FAQ's" },
            { command: "support", description: "🧑‍💻 Support" },
            { command: "help", description: "📋 Commands" },
        ]);

        // Register webhook
        const baseUrl = process.env.API_BASE_URL ?? `https://${req.hostname}`;
        const webhookUrl = `${baseUrl}/bot/telegram/webhook`;
        await client.setWebhook(webhookUrl, env.TG_WEBHOOK_SECRET, ["message", "callback_query"]);

        res.json({
            status: "ok",
            webhook: webhookUrl,
            commands: ["start", "mycards", "profile", "fund", "faq", "support"],
        });
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
});

// ── Ops Metrics endpoint ───────────────────────────────────

botRouter.get("/ops/metrics", async (req, res) => {
    const opsKey = env.OPS_API_KEY;
    if (!opsKey || req.header("X-Ops-Key") !== opsKey) {
        res.status(401).json({ error: "Unauthorized" });
        return;
    }

    try {
        const { MetricsService } = await import("./services/metricsService");
        const hours = parseInt(req.query.hours as string || "24", 10);
        const metrics = await MetricsService.collect(hours);
        res.json(metrics);
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
});

// ── Message Router ─────────────────────────────────────────

async function handleMessage(client: TelegramClient, msg: TgMessage): Promise<void> {
    if (!msg.text || !msg.from) return;

    const text = msg.text.trim();
    const cmd = normalizeCommand(text);
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    // Track command in admin bot (non-blocking)
    if (text.startsWith("/")) {
        AdminBot.botCommand(userId, text, msg.from.username).catch(() => {});
    }

    // /start with optional deep-link token
    if (cmd.startsWith("/start")) {
        const parts = text.split(" ");
        const token = parts.length > 1 ? parts[1] : undefined;
        await handleStartCommand(client, chatId, userId, token);
        return;
    }

    // Slash commands
    if (cmd === "/mycards" || text === "💳 My Cards") {
        await handleMyCardsCommand(client, chatId, userId);
        return;
    }

    if (cmd === "/fund" || text === "💰 Fund") {
        await handleFundCommand(client, chatId, userId);
        return;
    }

    if (cmd === "/profile" || text === "👤 Profile") {
        await handleProfileCommand(client, chatId, userId);
        return;
    }

    if (cmd === "/faq" || text === "❓ FAQ's") {
        await handleFaqCommand(client, chatId);
        return;
    }

    if (cmd === "/support" || text.startsWith("🧑‍💻") || text === "Support") {
        await handleSupportCommand(client, chatId);
        return;
    }

    if (cmd === "/help") {
        await client.sendMessage({
            chat_id: chatId,
            text:
                `<b>📋 ASG Card Bot — Commands</b>\n\n` +
                `/mycards — 💳 View and manage your cards\n` +
                `/fund — 💰 Fund a card\n` +
                `/profile — 👤 Edit email & phone\n` +
                `/faq — ❓ Frequently asked questions\n` +
                `/support — 🧑‍💻 Contact support\n` +
                `/help — 📋 Show this message\n\n` +
                `<i>First time? Link your wallet at</i> <a href="https://asgcard.dev">asgcard.dev</a>`,
            parse_mode: "HTML",
        });
        return;
    }

    // Check if this is a pending profile edit (email/phone input)
    if (userId) {
        const handled = await handleProfileInput(client, chatId, userId, text);
        if (handled) return;
    }

    // Unknown command or text — suggest /help
    if (text.startsWith("/")) {
        await client.sendMessage({
            chat_id: chatId,
            text: `Unknown command. Type /help to see available commands.`,
        });
    }
}

// ── Callback Router ────────────────────────────────────────

async function handleCallback(client: TelegramClient, cbq: TgCallbackQuery): Promise<void> {
    if (!cbq.data || !cbq.from) return;

    // Acknowledge immediately
    await client.answerCallbackQuery({ callback_query_id: cbq.id });

    const chatId = cbq.message?.chat.id;
    if (!chatId) return;

    // Noop callback (pagination counter button)
    if (cbq.data === "noop") return;

    // Delete reveal message
    if (cbq.data.startsWith("card_delete_msg:")) {
        const msgIdToDelete = parseInt(cbq.data.split(":")[1], 10);
        if (!isNaN(msgIdToDelete) && msgIdToDelete > 0) {
            await client.deleteMessage(chatId, msgIdToDelete).catch(() => {});
        }
        return;
    }

    // Validate callback data format (action:cardId[:extra...]) — skip for pagination
    const parts = cbq.data.split(":");
    if (parts.length >= 2 && !cbq.data.startsWith("cards_page:") && !isValidCardId(parts[1])) {
        appLogger.warn({ data: cbq.data }, "[Bot] Invalid cardId in callback_data");
        return;
    }

    // Route pagination callbacks — edit the current message in place
    if (cbq.data.startsWith("cards_page:")) {
        const page = parseInt(parts[1], 10);
        if (!isNaN(page) && page > 0) {
            const messageId = cbq.message?.message_id;
            await handleMyCardsCommand(client, chatId, cbq.from.id, page, messageId);
        }
        return;
    }

    // Route fund callbacks
    if (cbq.data.startsWith("fund_select:") || cbq.data.startsWith("fund_info:")) {
        await handleFundCallback(client, chatId, cbq.from.id, cbq.data);
        return;
    }

    // Route profile callbacks
    if (cbq.data.startsWith("profile_")) {
        await handleProfileCallback(client, chatId, cbq.from.id, cbq.data);
        return;
    }

    await handleCardCallback(client, chatId, cbq.from.id, cbq.data);
}

// ── Helpers ────────────────────────────────────────────────

function safeEqual(a: string, b: string): boolean {
    const bufA = Buffer.from(a, "utf-8");
    const bufB = Buffer.from(b, "utf-8");
    if (bufA.length !== bufB.length) return false;
    return crypto.timingSafeEqual(bufA, bufB);
}
