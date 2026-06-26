/**
 * Bot message templates — UX parity with CypherHQ reference screenshots.
 *
 * Dark style, emoji markers, compact format.
 * All templates use HTML parse_mode for reliable formatting.
 *
 * @module modules/bot/templates
 */

// ── Card Types ─────────────────────────────────────────────

interface CardSummary {
    cardId: string;
    nameOnCard: string;
    last4: string;
    balance: number;
    status: "active" | "frozen";
}

// ── Welcome / Link ─────────────────────────────────────────

export function welcomeMessage(): string {
    return (
        `Hey there from ASG Card! 👋\n\n` +
        `<b>Important:</b> Link your account to Telegram\n` +
        `Please link your Telegram account by using the bot command prefilled below in your chat.\n\n` +
        `If you couldn't find the bot command, use the manual linking option in Card Options at ` +
        `<a href="https://asgcard.dev/portal">asgcard.dev/portal</a>`
    );
}

export function linkSuccessMessage(walletShort: string): string {
    return (
        `✅ <b>Account linked successfully!</b>\n\n` +
        `Your wallet <code>${walletShort}</code> is now connected.\n` +
        `Tap <b>💳 My Cards</b> below to view your cards.`
    );
}

export function linkFailedMessage(reason: string): string {
    const reasonMap: Record<string, string> = {
        token_expired: "This link has expired. Please generate a new one from your portal.",
        token_already_consumed: "This link was already used. Please generate a new one from your portal.",
        token_revoked: "This link was revoked. Please generate a new one from your portal.",
        invalid_token: "Invalid link. Please generate a new one from your portal.",
    };

    return (
        `❌ <b>Linking failed</b>\n\n` +
        `${reasonMap[reason] ?? "Unknown error. Please try again."}\n\n` +
        `Visit <a href="https://asgcard.dev/portal">asgcard.dev/portal</a> to connect.`
    );
}

export function noBindingMessage(): string {
    return (
        `🔒 <b>Account not linked</b>\n\n` +
        `You have no cards associated with your account.\n\n` +
        `Link your wallet first at <a href="https://asgcard.dev/portal">asgcard.dev/portal</a>`
    );
}

// ── My Cards ───────────────────────────────────────────────

export function accountBalanceMessage(
    totalBalance: number,
    cards: CardSummary[]
): string {
    if (cards.length === 0) {
        return `You have no cards associated with your account.`;
    }

    let msg = `💳 <b>Account Balance</b> (USD): <b>$${totalBalance.toFixed(2)}</b>\n\n`;
    msg += `Please select a card:`;

    return msg;
}

export function cardListItem(card: CardSummary): string {
    const statusIcon = card.status === "frozen" ? "❄️" : "💳";
    return `${statusIcon} ASG Virtual Card - xxxx ${card.last4}`;
}

// ── Card Actions ───────────────────────────────────────────

export function cardFrozenMessage(last4: string): string {
    return `❄️ Card ending <b>${last4}</b> has been <b>frozen</b>.\nNo new transactions will be authorized.`;
}

export function cardUnfrozenMessage(last4: string): string {
    return `✅ Card ending <b>${last4}</b> has been <b>unfrozen</b>.\nTransactions are now enabled.`;
}

export function cardRevealLinkMessage(url: string): string {
    return (
        `👁 <b>Card Reveal</b>\n\n` +
        `Tap the secure link below to view your card details.\n` +
        `⚠️ This link expires in 60 seconds and can only be used once.\n\n` +
        `🔗 <a href="${url}">View Card Details</a>`
    );
}

// ── Statement ──────────────────────────────────────────────

interface StatementEntry {
    type: "debit" | "credit" | "decline" | "refund";
    merchant: string;
    amount: number;
    status: string;
    timestamp: string;
    txnId: string;
}

export function statementMessage(last4: string, entries: StatementEntry[]): string {
    if (entries.length === 0) {
        return `📊 <b>Statement</b> — Card xxxx ${last4}\n\nNo recent transactions.`;
    }

    let msg = `📊 <b>Statement</b> — Card xxxx ${last4}\n\n`;

    for (const e of entries) {
        const icon = e.type === "debit" ? "💳" : e.type === "decline" ? "❌" : e.type === "refund" ? "💰" : "💵";
        const sign = e.type === "credit" || e.type === "refund" ? "+" : "-";
        const date = new Date(e.timestamp).toLocaleDateString("en-US", { month: "short", day: "numeric" });
        msg += `${icon} ${date} | ${e.merchant} | ${sign}$${e.amount.toFixed(2)} | ${e.status}\n`;
    }

    return msg;
}

// ── Transaction Alerts ─────────────────────────────────────

export function chargeAlertMessage(
    last4: string,
    amount: number,
    merchant: string,
    balance: number,
    txnId: string
): string {
    return (
        `💳 Your ASG Card ending with XX${last4} has been charged ` +
        `${amount.toFixed(2)} USD to ${merchant}.\n` +
        `Available Bal: ${balance.toFixed(2)} USD Txn ID: ${txnId}`
    );
}

export function declineAlertMessage(
    last4: string,
    amount: number,
    merchant: string,
    reason: string,
    balance: number,
    txnId: string
): string {
    return (
        `❌ Your ASG Card ending in XX${last4} was declined for a ` +
        `${amount.toFixed(2)} USD purchase at ${merchant}. ` +
        `Reason: ${reason}.\n` +
        `Available Balance: ${balance.toFixed(2)} USD Txn ID: ${txnId}`
    );
}

export function refundAlertMessage(
    amount: number,
    merchant: string,
    txnId: string,
    newBalance: number
): string {
    return (
        `Your refund of amount $${amount.toFixed(2)} from ${merchant} ` +
        `(Transaction ID: ${txnId}) has been cleared. ` +
        `Your updated balance is $${newBalance.toFixed(2)}.`
    );
}

export function loadAlertMessage(
    last4: string,
    amount: number,
    newBalance: number
): string {
    return (
        `Your ASG Card Account has been loaded with ${amount.toFixed(2)} USD. ` +
        `Your new balance is ${newBalance.toFixed(2)} USD.`
    );
}

// ── FAQ / Support ──────────────────────────────────────────

export function faqMessage(): string {
    return (
        `<b>❓ Frequently Asked Questions</b>\n\n` +
        `<b>How do I create a card?</b>\n` +
        `Use our SDK: <code>client.createCard({ amount: 50, nameOnCard: 'AI', email: 'a@b.com' })</code>. ` +
        `Payment is automatic via x402 on Stellar.\n\n` +
        `<b>How do I fund my card?</b>\n` +
        `Use <code>client.fundCard({ amount: 25, cardId: 'uuid' })</code> to top up an existing card.\n\n` +
        `<b>What are the fees?</b>\n` +
        `Issuance: $3 (one-time). Top-up: $2.20–$12 based on amount. ASG service fee: $2–$7. ` +
        `Full breakdown at <a href="https://asgcard.dev/docs#pricing">asgcard.dev/docs#pricing</a>.\n\n` +
        `<b>How does x402 payment work?</b>\n` +
        `You send a request → get a 402 challenge → pay USDC on Stellar → retry with X-Payment proof. ` +
        `The SDK handles this automatically.\n\n` +
        `<b>Are Stellar fees sponsored?</b>\n` +
        `Yes! The x402 facilitator covers network fees. You only need USDC.\n\n` +
        `📚 Full docs: <a href="https://asgcard.dev/docs">asgcard.dev/docs</a>`
    );
}

export function supportMessage(): string {
    return (
        `Contact ASG Card Support at <a href="https://asgcard.dev">asgcard.dev</a>\n\n` +
        `📧 Email: support@asgcard.dev\n` +
        `🔒 Security issues: security@asgcard.dev`
    );
}
