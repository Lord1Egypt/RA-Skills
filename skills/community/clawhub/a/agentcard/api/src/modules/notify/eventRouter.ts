/**
 * Event Router — hooks into webhook processing to dispatch notifications.
 *
 * Called after webhook events are accepted and stored.
 *
 * @module modules/notify/eventRouter
 */

import { NotifyService, type CardEvent } from "./notifyService";
import { query } from "../../db/db";

/**
 * Process a webhook event for potential Telegram notification.
 * Called from the main webhook handler after the event is stored.
 */
export async function routeCardEvent(
    eventType: string,
    payload: Record<string, unknown>
): Promise<void> {
    // Extract card/wallet info from webhook payload
    const cardId = (payload.card_id ?? payload.cardId ?? "") as string;
    if (!cardId) return;

    // Look up wallet from card
    const cards = await query<{ wallet_address: string; card_number_last4: string }>(
        `SELECT wallet_address,
            RIGHT(card_number, 4) as card_number_last4
     FROM cards WHERE card_id = $1 LIMIT 1`,
        [cardId]
    );

    if (cards.length === 0) return;

    const card = cards[0];

    const event: CardEvent = {
        eventType,
        cardId,
        walletAddress: card.wallet_address,
        payload: {
            last4: card.card_number_last4,
            amount: payload.amount as number | undefined,
            merchant: payload.merchant as string | undefined,
            balance: payload.available_balance as number | undefined,
            txnId: payload.transaction_id as string | undefined,
            reason: payload.decline_reason as string | undefined,
            newBalance: payload.new_balance as number | undefined,
        },
    };

    await NotifyService.processEvent(event);
}

// Re-export for convenience
export { NotifyService };
