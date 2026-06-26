import crypto from "node:crypto";
import type { StoredCard } from "../types/domain";
import type { CardRepository, CreateCardInput } from "./types";

export class InMemoryCardRepository implements CardRepository {
    private cards = new Map<string, StoredCard>();

    async create(input: CreateCardInput): Promise<StoredCard> {
        const card: StoredCard = {
            cardId: `card_${crypto.randomUUID().slice(0, 8)}`,
            walletAddress: input.walletAddress,
            nameOnCard: input.nameOnCard,
            email: input.email,
            balance: input.initialAmountUsd,
            initialAmountUsd: input.initialAmountUsd,
            status: "active",
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            details: input.details,
            fourPaymentsId: input.fourPaymentsId,
        };

        this.cards.set(card.cardId, card);
        return card;
    }

    async findById(cardId: string): Promise<StoredCard | undefined> {
        return this.cards.get(cardId);
    }

    async findByWallet(walletAddress: string): Promise<StoredCard[]> {
        return Array.from(this.cards.values()).filter(
            (c) => c.walletAddress === walletAddress
        );
    }

    async updateStatus(cardId: string, status: "active" | "frozen"): Promise<boolean> {
        const card = this.cards.get(cardId);
        if (!card) return false;
        card.status = status;
        card.updatedAt = new Date().toISOString();
        return true;
    }

    async addBalance(cardId: string, usdAmount: number): Promise<boolean> {
        const card = this.cards.get(cardId);
        if (!card) return false;

        card.balance += usdAmount;
        card.updatedAt = new Date().toISOString();
        return true;
    }

    async setDetailsRevoked(cardId: string, revoked: boolean): Promise<boolean> {
        const card = this.cards.get(cardId);
        if (!card) return false;

        (card as any).detailsRevoked = revoked;
        card.updatedAt = new Date().toISOString();
        return true;
    }

    private nonces = new Map<string, { wallet: string, cardId: string, timestamp: number }>();

    // REALIGN-003: Atomic Nonce & Rate Limit check
    async recordNonceAndCheckRateLimit(walletAddress: string, cardId: string, nonce: string, limitPerHour: number): Promise<{
        allowed: boolean;
        reason?: 'replay' | 'rate_limit';
        retryAfterSeconds?: number;
    }> {
        if (this.nonces.has(nonce)) {
            return { allowed: false, reason: 'replay' };
        }

        const now = Date.now();
        const hourAgo = now - 3600000;
        let count = 0;
        for (const v of this.nonces.values()) {
            if (v.cardId === cardId && v.timestamp >= hourAgo) count++;
        }
        if (count >= limitPerHour) {
            return { allowed: false, reason: 'rate_limit', retryAfterSeconds: 3600 };
        }

        this.nonces.set(nonce, { wallet: walletAddress, cardId, timestamp: now });
        return { allowed: true };
    }
}
