/**
 * Alert Delivery Service — routes 4payments webhook events to Telegram users.
 *
 * Flow: 4payments webhook → event parsed → find card owner → find TG binding → send alert.
 *
 * @module modules/bot/services/alertService
 */

import { query } from "../../../db/db";
import { appLogger } from "../../../utils/logger";
import {
    chargeAlertMessage,
    declineAlertMessage,
    refundAlertMessage,
    loadAlertMessage,
} from "../templates";

// ── Types ──────────────────────────────────────────────────

export interface CardEvent {
    type: string;
    cardId?: string;
    externalCardId?: string;
    fourPaymentsId?: string;
    amount?: number;
    merchant?: string;
    balance?: number;
    reason?: string;
    txnId?: string;
    last4?: string;
    payload: Record<string, unknown>;
}

// ── Service ────────────────────────────────────────────────

export class AlertService {
    /**
     * Process a 4payments webhook event and deliver as Telegram alert.
     * Returns true if alert was delivered, false if no binding found or event type ignored.
     */
    static async deliverAlert(
        event: CardEvent,
        sendMessage: (chatId: number, text: string) => Promise<void>
    ): Promise<boolean> {
        // Extract card identifiers from the event
        const fpId =
            event.fourPaymentsId ??
            (event.payload.card_id as string) ??
            (event.payload.cardId as string) ??
            null;

        const extId =
            event.externalCardId ??
            (event.payload.external_card_id as string) ??
            (event.payload.externalCardId as string) ??
            null;

        if (!fpId && !extId) {
            appLogger.warn({ event: event.type }, "[AlertService] No card ID in event, skipping");
            return false;
        }

        // Look up the card and its owner wallet
        let ownerWallet: string | null = null;
        let last4 = event.last4 ?? "????";

        if (fpId) {
            const rows = await query<{ wallet_address: string; card_number_last4: string }>(
                `SELECT wallet_address, 
                        COALESCE(RIGHT(card_number, 4), 'XXXX') as card_number_last4
                 FROM cards 
                 WHERE four_payments_id = $1 
                 LIMIT 1`,
                [fpId]
            ).catch(() => []);
            if (rows.length > 0) {
                ownerWallet = rows[0].wallet_address;
                last4 = rows[0].card_number_last4 || last4;
            }
        }

        if (!ownerWallet && extId) {
            const rows = await query<{ wallet_address: string; card_number_last4: string }>(
                `SELECT wallet_address,
                        COALESCE(RIGHT(card_number, 4), 'XXXX') as card_number_last4
                 FROM cards 
                 WHERE card_id = $1 
                 LIMIT 1`,
                [extId]
            ).catch(() => []);
            if (rows.length > 0) {
                ownerWallet = rows[0].wallet_address;
                last4 = rows[0].card_number_last4 || last4;
            }
        }

        if (!ownerWallet) {
            appLogger.warn({ fpId, extId }, "[AlertService] Card not found in DB, skipping alert");
            return false;
        }

        // Find Telegram binding for this wallet
        const bindings = await query<{ chat_id: string }>(
            `SELECT chat_id 
             FROM owner_telegram_links 
             WHERE owner_wallet = $1 AND status = 'active'`,
            [ownerWallet]
        ).catch(() => []);

        if (bindings.length === 0) {
            appLogger.info({ ownerWallet }, "[AlertService] No TG binding for wallet, skipping");
            return false;
        }

        const chatId = Number(bindings[0].chat_id);

        // Build alert message based on event type
        const amount = event.amount ?? (event.payload.amount as number) ?? 0;
        const merchant =
            event.merchant ??
            (event.payload.merchant as string) ??
            (event.payload.merchant_name as string) ??
            "Unknown";
        const balance = event.balance ?? (event.payload.balance as number) ?? 0;
        const reason = event.reason ?? (event.payload.reason as string) ?? "Unknown";
        const txnId =
            event.txnId ??
            (event.payload.transaction_id as string) ??
            (event.payload.id as string) ??
            "N/A";

        let message: string;

        switch (event.type) {
            case "card.transaction":
            case "card.charge":
            case "TRANSACTION":
                message = chargeAlertMessage(last4, amount, merchant, balance, txnId);
                break;

            case "card.decline":
            case "card.declined":
                message = declineAlertMessage(last4, amount, merchant, reason, balance, txnId);
                break;

            case "card.refund":
            case "card.reversal":
                message = refundAlertMessage(amount, merchant, txnId, balance);
                break;

            case "card.load":
            case "card.funded":
            case "card.topup":
                message = loadAlertMessage(last4, amount, balance);
                break;

            case "CARD-ISSUE":
            case "card.created":
                message = `🎉 New ASG Card xxxx ${last4} has been issued and is ready to use!`;
                break;

            case "EXTRAFEE":
            case "card.fee":
                message = `💰 Fee of $${amount.toFixed(2)} applied to card xxxx ${last4}. Balance: $${balance.toFixed(2)}`;
                break;

            default:
                appLogger.info({ type: event.type }, "[AlertService] Unhandled event type");
                return false;
        }

        // Record alert in bot_events for metrics
        await query(
            `INSERT INTO bot_events (idempotency_key, event_type, payload_hash, delivery_status)
             VALUES ($1, $2, $3, 'pending')
             ON CONFLICT (idempotency_key) DO NOTHING`,
            [`${event.type}:${fpId ?? extId}:${txnId}`, event.type, txnId]
        ).catch(() => {});

        // Deliver alert
        try {
            await sendMessage(chatId, message);

            // Update delivery status
            await query(
                `UPDATE bot_events 
                 SET delivery_status = 'delivered' 
                 WHERE idempotency_key = $1`,
                [`${event.type}:${fpId ?? extId}:${txnId}`]
            ).catch(() => {});

            appLogger.info({ chatId, type: event.type }, "[AlertService] Alert delivered");
            return true;
        } catch (error) {
            appLogger.error({ err: error, chatId }, "[AlertService] Failed to deliver alert");

            await query(
                `UPDATE bot_events 
                 SET delivery_status = 'failed' 
                 WHERE idempotency_key = $1`,
                [`${event.type}:${fpId ?? extId}:${txnId}`]
            ).catch(() => {});

            return false;
        }
    }
}
