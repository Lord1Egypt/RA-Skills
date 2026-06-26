/**
 * Profile command handler — view and edit email/phone.
 *
 * /profile shows current profile info with Edit buttons.
 * Tapping Edit Email or Edit Phone triggers a conversational flow
 * where the bot asks for the new value and saves it.
 *
 * @module modules/bot/commands/profile
 */

import type { TelegramClient } from "../telegramClient";
import { requireOwnerBinding } from "../../authz/ownerPolicy";
import { query } from "../../../db/db";
import {
    noBindingMessage,
} from "../templates";
import { persistentMenu } from "../keyboards";
import { escapeHtml } from "../../../utils/html";

// ── Pending edits (in-memory, per chat) ───────────────────
// On Vercel serverless this resets on cold start, but that's acceptable —
// worst case user has to tap Edit again.
const pendingEdits = new Map<number, { field: "email" | "phone"; userId: number }>();

// ── Profile Command ────────────────────────────────────────

export async function handleProfileCommand(
    client: TelegramClient,
    chatId: number,
    userId: number
): Promise<void> {
    const owner = await requireOwnerBinding(userId, "profile");
    if (!owner) {
        await client.sendMessage({
            chat_id: chatId,
            text: noBindingMessage(),
            parse_mode: "HTML",
            reply_markup: persistentMenu(),
        });
        return;
    }

    // Fetch current profile data
    const rows = await query<{ email: string | null; phone: string | null }>(
        `SELECT email, phone FROM owner_telegram_links
         WHERE telegram_user_id = $1 AND status = 'active' LIMIT 1`,
        [userId]
    );

    const profile = rows[0] || { email: null, phone: null };

    const emailDisplay = profile.email || "—  not set";
    const phoneDisplay = profile.phone || "—  not set";

    const text =
        `👤 <b>Profile</b>\n\n` +
        `📧 Email: <b>${escapeHtml(emailDisplay)}</b>\n` +
        `📱 Phone: <b>${escapeHtml(phoneDisplay)}</b>\n\n` +
        `<i>Tap a button to update</i>`;

    await client.sendMessage({
        chat_id: chatId,
        text,
        parse_mode: "HTML",
        reply_markup: {
            inline_keyboard: [
                [
                    { text: "📧 Edit Email", callback_data: "profile_edit:email" },
                    { text: "📱 Edit Phone", callback_data: "profile_edit:phone" },
                ],
            ],
        },
    });
}

// ── Profile Callback ───────────────────────────────────────

export async function handleProfileCallback(
    client: TelegramClient,
    chatId: number,
    userId: number,
    data: string
): Promise<void> {
    if (data === "profile_edit:email") {
        pendingEdits.set(chatId, { field: "email", userId });
        await client.sendMessage({
            chat_id: chatId,
            text: "📧 Send me your new <b>email address</b>:",
            parse_mode: "HTML",
            reply_markup: {
                inline_keyboard: [
                    [{ text: "❌ Cancel", callback_data: "profile_cancel" }],
                ],
            },
        });
    } else if (data === "profile_edit:phone") {
        pendingEdits.set(chatId, { field: "phone", userId });
        await client.sendMessage({
            chat_id: chatId,
            text: "📱 Send me your new <b>phone number</b>:",
            parse_mode: "HTML",
            reply_markup: {
                inline_keyboard: [
                    [{ text: "❌ Cancel", callback_data: "profile_cancel" }],
                ],
            },
        });
    } else if (data === "profile_cancel") {
        pendingEdits.delete(chatId);
        await client.sendMessage({
            chat_id: chatId,
            text: "❌ Edit cancelled.",
        });
    }
}

// ── Handle Text Input (for pending edits) ──────────────────

export async function handleProfileInput(
    client: TelegramClient,
    chatId: number,
    userId: number,
    text: string
): Promise<boolean> {
    const pending = pendingEdits.get(chatId);
    if (!pending || pending.userId !== userId) return false;

    const { field } = pending;
    pendingEdits.delete(chatId);

    // Basic validation
    const value = text.trim();

    if (field === "email") {
        // Simple email validation
        if (!value.includes("@") || !value.includes(".")) {
            await client.sendMessage({
                chat_id: chatId,
                text: "⚠️ Invalid email format. Please try again via /profile.",
            });
            return true;
        }
    }

    if (field === "phone") {
        // Allow digits, +, spaces, dashes, parens
        const cleaned = value.replace(/[\s\-\(\)]/g, "");
        if (!/^\+?\d{7,15}$/.test(cleaned)) {
            await client.sendMessage({
                chat_id: chatId,
                text: "⚠️ Invalid phone format. Use international format like +1234567890. Try again via /profile.",
            });
            return true;
        }
    }

    // Update profile in DB
    const column = field === "email" ? "email" : "phone";
    await query(
        `UPDATE owner_telegram_links SET ${column} = $1 WHERE telegram_user_id = $2 AND status = 'active'`,
        [value, userId]
    );

    // Reverse sync: if email changed, update all cards for this wallet
    if (field === "email") {
        try {
            const walletRows = await query<{ owner_wallet: string }>(
                `SELECT owner_wallet FROM owner_telegram_links WHERE telegram_user_id = $1 AND status = 'active' LIMIT 1`,
                [userId]
            );
            if (walletRows.length > 0) {
                await query(
                    `UPDATE cards SET email = $1 WHERE wallet_address = $2`,
                    [value, walletRows[0].owner_wallet]
                );
            }
        } catch (err) {
            // Non-fatal — profile is updated, card sync is best-effort
            console.error("[profile] Cards email sync failed:", err);
        }
    }

    const icon = field === "email" ? "📧" : "📱";
    await client.sendMessage({
        chat_id: chatId,
        text: `✅ ${icon} ${field === "email" ? "Email" : "Phone"} updated to <b>${escapeHtml(value)}</b>`,
        parse_mode: "HTML",
    });

    return true;
}
