/**
 * Support command handler.
 *
 * @module modules/bot/commands/support
 */

import type { TelegramClient } from "../telegramClient";
import { supportMessage } from "../templates";
import { persistentMenu } from "../keyboards";

export async function handleSupportCommand(
    client: TelegramClient,
    chatId: number
): Promise<void> {
    await client.sendMessage({
        chat_id: chatId,
        text: supportMessage(),
        parse_mode: "HTML",
        reply_markup: persistentMenu(),
        disable_web_page_preview: true,
    });
}
