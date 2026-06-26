/**
 * Fund command handler — shows fund options and deep-links to SDK/API.
 *
 * Since funding requires x402 payment (on-chain USDC), the bot
 * provides card selection + funding info with deep-link to the API.
 *
 * @module modules/bot/commands/fund
 */

import type { TelegramClient } from "../telegramClient";
import { requireOwnerBinding } from "../../authz/ownerPolicy";
import { cardService, HttpError } from "../../../services/cardService";
import { persistentMenu } from "../keyboards";
import { FUNDING_TIERS } from "../../../config/pricing";

// ── Types ──────────────────────────────────────────────────

interface FundTier {
    label: string;
    amount: number;
    totalCost: number;
}

// ── Fund Command ───────────────────────────────────────────

export async function handleFundCommand(
    client: TelegramClient,
    chatId: number,
    userId: number
): Promise<void> {
    // Verify binding
    const owner = await requireOwnerBinding(userId, "fund_cards");

    if (!owner) {
        await client.sendMessage({
            chat_id: chatId,
            text: "🔐 You need to link your wallet first.\nUse the portal at https://asgcard.dev to connect your Telegram.",
            reply_markup: persistentMenu(),
        });
        return;
    }

    try {
        const cards = await cardService.listCards(owner.ownerWallet);

        if (cards.length === 0) {
            await client.sendMessage({
                chat_id: chatId,
                text: "📭 You don't have any cards yet.\n\nCreate one using the SDK:\n<code>client.createCard({ amount: 50, nameOnCard: 'AI', email: 'a@b.com' })</code>",
                parse_mode: "HTML",
                reply_markup: persistentMenu(),
            });
            return;
        }

        // Build card selection keyboard for funding
        const buttons = cards
            .filter((c) => c.status === "active")
            .map((c) => [
                {
                    text: `💳 xxxx ${c.lastFour} — $${c.balance.toFixed(2)}`,
                    callback_data: `fund_select:${c.cardId}`,
                },
            ]);

        if (buttons.length === 0) {
            await client.sendMessage({
                chat_id: chatId,
                text: "❄️ All your cards are frozen. Unfreeze a card first to fund it.",
                reply_markup: persistentMenu(),
            });
            return;
        }

        await client.sendMessage({
            chat_id: chatId,
            text: "<b>💰 Fund a Card</b>\n\nSelect a card to see funding options:",
            parse_mode: "HTML",
            reply_markup: { inline_keyboard: buttons },
        });
    } catch (error) {
        const msg =
            error instanceof HttpError
                ? `⚠️ ${error.message}`
                : "⚠️ Something went wrong. Please try again.";
        await client.sendMessage({ chat_id: chatId, text: msg });
    }
}

// ── Fund Callbacks ─────────────────────────────────────────

export async function handleFundCallback(
    client: TelegramClient,
    chatId: number,
    userId: number,
    data: string
): Promise<void> {
    const parts = data.split(":");
    const action = parts[0];
    const cardId = parts[1];
    if (!cardId) return;

    const owner = await requireOwnerBinding(userId, "fund_card_action");
    if (!owner) {
        await client.sendMessage({
            chat_id: chatId,
            text: "🔐 Session expired. Please /start again.",
        });
        return;
    }

    if (action === "fund_select") {
        await showFundTiers(client, chatId, owner.ownerWallet, cardId);
    } else if (action === "fund_info") {
        const amount = Number(parts[2]);
        await showFundDetails(client, chatId, owner.ownerWallet, cardId, amount);
    }
}

// ── Fund Details (tier selected) ───────────────────────────

async function showFundDetails(
    client: TelegramClient,
    chatId: number,
    wallet: string,
    cardId: string,
    amount: number
): Promise<void> {
    try {
        const tier = FUNDING_TIERS.find((t) => t.fundAmount === amount);
        if (!tier) {
            await client.sendMessage({
                chat_id: chatId,
                text: "⚠️ Invalid funding tier.",
            });
            return;
        }

        const result = await cardService.getCard(wallet, cardId);
        const last4 = result.card.lastFour;

        const fundEndpoint = `https://api.asgcard.dev${tier.endpoint}`;

        await client.sendMessage({
            chat_id: chatId,
            text:
                `<b>💰 Fund Card xxxx ${last4}</b>\n\n` +
                `<b>Load Amount:</b> $${tier.fundAmount.toFixed(2)}\n` +
                `<b>Top-up Fee:</b> $${tier.topUpFee.toFixed(2)}\n` +
                `<b>Service Fee:</b> $${tier.serviceFee.toFixed(2)}\n` +
                `<b>Total USDC Cost:</b> $${tier.totalCost.toFixed(2)}\n\n` +
                `<i>Payment: USDC on Stellar via x402 protocol</i>\n\n` +
                `To fund this card, use the SDK or API:\n` +
                `<code>POST ${tier.endpoint}</code>\n` +
                `with the card ID and x402 payment header.\n\n` +
                `📖 <a href="https://docs.asgcard.dev/api/fund">Documentation</a>`,
            parse_mode: "HTML",
            reply_markup: {
                inline_keyboard: [
                    [
                        {
                            text: "⬅️ Back to tiers",
                            callback_data: `fund_select:${cardId}`,
                        },
                    ],
                ],
            },
        });
    } catch (error) {
        const msg =
            error instanceof HttpError
                ? `⚠️ ${error.message}`
                : "⚠️ Something went wrong.";
        await client.sendMessage({ chat_id: chatId, text: msg });
    }
}

// ── Fund Tiers Display ─────────────────────────────────────

async function showFundTiers(
    client: TelegramClient,
    chatId: number,
    wallet: string,
    cardId: string
): Promise<void> {
    try {
        const result = await cardService.getCard(wallet, cardId);
        const last4 = result.card.lastFour;

        // Build tier buttons from FUNDING_TIERS config
        const fundTiers: FundTier[] = FUNDING_TIERS.map((t) => ({
            label: `$${t.fundAmount}`,
            amount: t.fundAmount,
            totalCost: t.totalCost,
        }));

        const tierButtons = fundTiers.map((tier) => [
            {
                text: `${tier.label} (cost: $${tier.totalCost.toFixed(2)})`,
                callback_data: `fund_info:${cardId}:${tier.amount}`,
            },
        ]);

        await client.sendMessage({
            chat_id: chatId,
            text:
                `<b>💰 Fund Card xxxx ${last4}</b>\n` +
                `Current Balance: <b>$${result.card.balance.toFixed(2)}</b>\n\n` +
                `Select a funding amount:\n` +
                `<i>Payment is via USDC on Stellar (x402 protocol).</i>\n` +
                `<i>Use the SDK for programmatic funding.</i>`,
            parse_mode: "HTML",
            reply_markup: { inline_keyboard: tierButtons },
        });
    } catch (error) {
        const msg =
            error instanceof HttpError
                ? `⚠️ ${error.message}`
                : "⚠️ Something went wrong.";
        await client.sendMessage({ chat_id: chatId, text: msg });
    }
}
