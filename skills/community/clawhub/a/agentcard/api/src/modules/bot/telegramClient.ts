import { appLogger } from "../../utils/logger";
/**
 * Telegram Bot API client — minimal wrapper using native fetch.
 * No external dependencies.
 *
 * @module modules/bot/telegramClient
 */

// ── Types ──────────────────────────────────────────────────

export interface TgSendMessageParams {
    chat_id: number;
    text: string;
    parse_mode?: "HTML" | "Markdown" | "MarkdownV2";
    reply_markup?: TgReplyMarkup;
    disable_web_page_preview?: boolean;
}

export interface TgAnswerCallbackParams {
    callback_query_id: string;
    text?: string;
    show_alert?: boolean;
}

export interface TgInlineButton {
    text: string;
    callback_data?: string;
    url?: string;
}

export type TgReplyMarkup =
    | { inline_keyboard: TgInlineButton[][] }
    | { keyboard: { text: string }[][]; resize_keyboard?: boolean; one_time_keyboard?: boolean };

export interface TgUpdate {
    update_id: number;
    message?: TgMessage;
    callback_query?: TgCallbackQuery;
}

export interface TgMessage {
    message_id: number;
    from?: TgUser;
    chat: TgChat;
    text?: string;
    date: number;
}

export interface TgCallbackQuery {
    id: string;
    from: TgUser;
    message?: TgMessage;
    data?: string;
}

export interface TgUser {
    id: number;
    is_bot: boolean;
    first_name: string;
    last_name?: string;
    username?: string;
}

export interface TgChat {
    id: number;
    type: "private" | "group" | "supergroup" | "channel";
}

export interface TgApiResponse<T = unknown> {
    ok: boolean;
    result?: T;
    description?: string;
    error_code?: number;
}

// ── Client ─────────────────────────────────────────────────

export class TelegramClient {
    private readonly baseUrl: string;

    constructor(private readonly token: string) {
        this.baseUrl = `https://api.telegram.org/bot${token}`;
    }

    /** Send a text message to a chat. Returns message_id on success. */
    async sendMessage(params: TgSendMessageParams): Promise<number | null> {
        const resp = await this.call<TgMessage>("sendMessage", params);
        return resp?.message_id ?? null;
    }

    /** Answer a callback query (removes "loading" spinner). */
    async answerCallbackQuery(params: TgAnswerCallbackParams): Promise<boolean> {
        const resp = await this.call<boolean>("answerCallbackQuery", params);
        return resp ?? false;
    }

    /** Edit an existing message text. */
    async editMessageText(params: {
        chat_id: number;
        message_id: number;
        text: string;
        parse_mode?: string;
        reply_markup?: TgReplyMarkup;
    }): Promise<boolean> {
        const resp = await this.call("editMessageText", params);
        return resp !== null;
    }

    /** Delete a message from chat. */
    async deleteMessage(chatId: number, messageId: number): Promise<boolean> {
        const resp = await this.call("deleteMessage", { chat_id: chatId, message_id: messageId });
        return resp !== null;
    }

    /** Set bot commands for the menu. */
    async setMyCommands(commands: { command: string; description: string }[]): Promise<boolean> {
        const resp = await this.call<boolean>("setMyCommands", { commands });
        return resp ?? false;
    }

    /** Register a webhook URL. */
    async setWebhook(url: string, secretToken?: string, allowedUpdates?: string[]): Promise<boolean> {
        const params: Record<string, unknown> = { url };
        if (secretToken) params.secret_token = secretToken;
        if (allowedUpdates) params.allowed_updates = allowedUpdates;
        const resp = await this.call<boolean>("setWebhook", params);
        return resp ?? false;
    }

    /** Get current webhook info (for health checks). */
    async getWebhookInfo(): Promise<{
        url: string;
        pending_update_count: number;
        last_error_date?: number;
        last_error_message?: string;
    }> {
        const resp = await this.call<{
            url: string;
            pending_update_count: number;
            last_error_date?: number;
            last_error_message?: string;
        }>("getWebhookInfo", {});
        return resp ?? { url: "", pending_update_count: 0 };
    }

    /** Remove the webhook. */
    async deleteWebhook(): Promise<boolean> {
        const resp = await this.call<boolean>("deleteWebhook", {});
        return resp ?? false;
    }

    /** Low-level API call. */
    private async call<T>(method: string, body: object): Promise<T | null> {
        try {
            const resp = await fetch(`${this.baseUrl}/${method}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });

            const data = (await resp.json()) as TgApiResponse<T>;

            if (!data.ok) {
                appLogger.error({ err: data.description ?? "unknown error" }, `[TG] ${method} failed:`);
                return null;
            }

            return data.result ?? null;
        } catch (error) {
            appLogger.error({ err: error }, `[TG] ${method} error`);
            return null;
        }
    }
}
