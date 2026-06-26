/**
 * Bot Gateway Module — public interface
 *
 * Handles Telegram webhook, bot commands, inline keyboards,
 * and message rendering. All bot functionality is accessed
 * through this module's exported router.
 *
 * @module modules/bot
 */
export { botRouter } from "./webhook";
export { TelegramClient } from "./telegramClient";
