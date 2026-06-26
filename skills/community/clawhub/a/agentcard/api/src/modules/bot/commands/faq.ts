/**
 * FAQ command handler.
 *
 * @module modules/bot/commands/faq
 */

import type { TelegramClient } from "../telegramClient";
import { faqMessage } from "../templates";
import { persistentMenu } from "../keyboards";

export async function handleFaqCommand(
    client: TelegramClient,
    chatId: number
): Promise<void> {
    await client.sendMessage({
        chat_id: chatId,
        text: faqMessage(),
        parse_mode: "HTML",
        reply_markup: persistentMenu(),
        disable_web_page_preview: false,
    });
}
