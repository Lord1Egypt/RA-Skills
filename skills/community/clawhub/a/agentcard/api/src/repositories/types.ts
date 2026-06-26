import type { StoredCard, TierAmount, CardDetails } from "../types/domain";

// ── Card Repository ────────────────────────────────────────

export interface CreateCardInput {
    walletAddress: string;
    nameOnCard: string;
    email: string;
    initialAmountUsd: number;
    tierAmount: TierAmount;
    txHash: string;
    details: CardDetails;
    fourPaymentsId?: string;
}

export interface CardRepository {
    create(input: CreateCardInput): Promise<StoredCard>;
    findById(cardId: string): Promise<StoredCard | undefined>;
    findByWallet(walletAddress: string): Promise<StoredCard[]>;
    updateStatus(cardId: string, status: "active" | "frozen"): Promise<boolean>;
    addBalance(cardId: string, usdAmount: number): Promise<boolean>;
    setDetailsRevoked(cardId: string, revoked: boolean): Promise<boolean>;

    // REALIGN-003: Atomic Nonce & Rate Limit check
    recordNonceAndCheckRateLimit(walletAddress: string, cardId: string, nonce: string, limitPerHour: number): Promise<{
        allowed: boolean;
        reason?: 'replay' | 'rate_limit';
        retryAfterSeconds?: number;
    }>;
}
// ── Payment Repository ─────────────────────────────────────

export type PaymentStatus =
    | "proof_received"
    | "verified"
    | "settled"
    | "settle_failed"
    | "verify_failed";

export interface PaymentRecord {
    id: string;
    txHash: string;
    payer: string;
    amount: string;
    tierAmount: TierAmount;
    status: PaymentStatus;
    settleId?: string;
    cardId?: string;
    createdAt: string;
    updatedAt: string;
}

export interface PaymentRepository {
    recordPayment(payment: Omit<PaymentRecord, "id" | "createdAt" | "updatedAt">): Promise<{ record: PaymentRecord; inserted: boolean }>;
    findByTxHash(txHash: string): Promise<PaymentRecord | undefined>;
    markSettled(txHash: string, settleId: string): Promise<boolean>;
    markFailed(txHash: string, status: "settle_failed" | "verify_failed"): Promise<boolean>;
}

// ── Webhook Event Repository ───────────────────────────────

export interface WebhookEventRecord {
    id: string;
    idempotencyKey: string;
    eventType: string;
    payload: Record<string, unknown>;
    processedAt: string;
}

export interface WebhookEventRepository {
    store(event: Omit<WebhookEventRecord, "id" | "processedAt">): Promise<{ record: WebhookEventRecord; inserted: boolean }>;
    findByIdempotencyKey(key: string): Promise<WebhookEventRecord | undefined>;
}
