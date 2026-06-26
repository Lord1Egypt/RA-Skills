/**
 * /start command handler.
 *
 * Handles:
 * 1. /start lnk_<token> → consume token, create binding
 * 2. /start (no token) → welcome message with link instructions
 *
 * @module modules/bot/commands/start
 */

import type { TelegramClient } from "../telegramClient";
import { LinkService } from "../../portal/linkService";
import { AdminBot } from "../../admin/adminBot";
import {
    welcomeMessage,
    linkSuccessMessage,
    linkFailedMessage,
} from "../templates";
import { persistentMenu } from "../keyboards";

export async function handleStartCommand(
    client: TelegramClient,
    chatId: number,
    userId: number,
    token?: string
): Promise<void> {
    // Deep-link: /start lnk_<token>
    if (token && token.startsWith("lnk_")) {
        const result = await LinkService.consumeToken(token, userId, chatId);

        if (result.success && result.ownerWallet) {
            const walletShort =
                result.ownerWallet.substring(0, 6) +
                "..." +
                result.ownerWallet.substring(result.ownerWallet.length - 4);

            await client.sendMessage({
                chat_id: chatId,
                text: linkSuccessMessage(walletShort),
                parse_mode: "HTML",
                reply_markup: persistentMenu(),
            });

            // Notify admin bot
            AdminBot.accountLinked({
                wallet: result.ownerWallet,
                telegramUserId: userId,
                username: undefined,
            }).catch(() => {});
        } else {
            await client.sendMessage({
                chat_id: chatId,
                text: linkFailedMessage(result.error ?? "unknown"),
                parse_mode: "HTML",
                reply_markup: persistentMenu(),
            });
        }
        return;
    }

    // Plain /start — welcome
    await client.sendMessage({
        chat_id: chatId,
        text: welcomeMessage(),
        parse_mode: "HTML",
        reply_markup: persistentMenu(),
    });
}
