/**
 * Inline keyboard builders — persistent menu + card actions.
 *
 * @module modules/bot/keyboards
 */

import type { TgInlineButton, TgReplyMarkup } from "./telegramClient";

// ── Persistent Bottom Menu (Reply Keyboard) ────────────────

export function persistentMenu(): TgReplyMarkup {
    return {
        keyboard: [
            [{ text: "💳 My Cards" }, { text: "👤 Profile" }],
            [{ text: "❓ FAQ's" }, { text: "🧑‍💻 Support" }],
        ],
        resize_keyboard: true,
        one_time_keyboard: false,
    };
}

// ── Card Selection ─────────────────────────────────────────

export function cardSelectionKeyboard(
    cards: { cardId: string; last4: string; status: string }[]
): TgReplyMarkup {
    const buttons: TgInlineButton[][] = cards.map((c) => [
        {
            text: `💳 ASG Virtual Card - xxxx ${c.last4}`,
            callback_data: `card_select:${c.cardId}`,
        },
    ]);

    return { inline_keyboard: buttons };
}

// ── Card Actions ───────────────────────────────────────────

export function cardActionsKeyboard(
    cardId: string,
    currentStatus: "active" | "frozen"
): TgReplyMarkup {
    const freezeBtn: TgInlineButton =
        currentStatus === "active"
            ? { text: "❄️ Freeze Card", callback_data: `card_freeze:${cardId}` }
            : { text: "🔥 Unfreeze Card", callback_data: `card_unfreeze:${cardId}` };

    return {
        inline_keyboard: [
            [{ text: "👁 Card Reveal", callback_data: `card_reveal:${cardId}` }],
            [
                freezeBtn,
                { text: "📊 Statement", callback_data: `card_statement:${cardId}` },
            ],
        ],
    };
}

// ── Confirm / Cancel ───────────────────────────────────────

export function confirmKeyboard(
    action: string,
    resourceId: string
): TgReplyMarkup {
    return {
        inline_keyboard: [
            [
                { text: "✅ Confirm", callback_data: `confirm:${action}:${resourceId}` },
                { text: "❌ Cancel", callback_data: `cancel:${action}:${resourceId}` },
            ],
        ],
    };
}
