/**
 * Persistence integration tests.
 *
 * These run against the configured REPO_MODE repositories.
 * In CI/default: inmemory. With DATABASE_URL: postgres.
 *
 * Tests cover:
 *   - Card CRUD (create, findById, findByWallet, addBalance, updateStatus)
 *   - Payment anti-replay (recordPayment, findByTxHash, concurrent dupes)
 *   - Payment settle transitions (settled, settle_failed, verify_failed)
 *   - Webhook idempotency (store, findByKey, concurrent dupes)
 */
import { describe, it, expect, afterAll } from "vitest";
import { cardRepository, paymentRepository, webhookEventRepository } from "../src/repositories/runtime";
import type { CardDetails, TierAmount } from "../src/types/domain";

// Pool cleanup for postgres mode
afterAll(async () => {
    if (process.env.REPO_MODE === "postgres") {
        const { closePool } = await import("../src/db/db");
        await closePool();
    }
});

// ── Test fixtures ──────────────────────────────────────────

const testDetails: CardDetails = {
    cardNumber: "4111111111111111",
    expiryMonth: 12,
    expiryYear: 2028,
    cvv: "123",
    billingAddress: {
        street: "123 Test St",
        city: "Testville",
        state: "TS",
        zip: "12345",
        country: "US"
    }
};

// ── Card Repository Tests ──────────────────────────────────

describe("CardRepository", () => {
    let createdCardId: string;

    it("create() → returns StoredCard with correct fields", async () => {
        const card = await cardRepository.create({
            walletAddress: "GTEST1111111111111111111111111111111111111111111111111111",
            nameOnCard: "Test User",
            email: "test@example.com",
            initialAmountUsd: 25,
            tierAmount: 25 as TierAmount,
            txHash: `tx_card_create_${Date.now()}`,
            details: testDetails
        });

        expect(card.cardId).toMatch(/^card_/);
        expect(card.walletAddress).toBe("GTEST1111111111111111111111111111111111111111111111111111");
        expect(card.nameOnCard).toBe("Test User");
        expect(card.email).toBe("test@example.com");
        expect(card.balance).toBe(25);
        expect(card.initialAmountUsd).toBe(25);
        expect(card.status).toBe("active");
        expect(card.details.cardNumber).toBe("4111111111111111");
        expect(card.createdAt).toBeTruthy();

        createdCardId = card.cardId;
    });

    it("findById() → returns card by ID", async () => {
        const card = await cardRepository.findById(createdCardId);
        expect(card).toBeDefined();
        expect(card!.cardId).toBe(createdCardId);
    });

    it("findById() → returns undefined for non-existent ID", async () => {
        const card = await cardRepository.findById("card_nonexistent");
        expect(card).toBeUndefined();
    });

    it("findByWallet() → returns cards for wallet", async () => {
        const cards = await cardRepository.findByWallet(
            "GTEST1111111111111111111111111111111111111111111111111111"
        );
        expect(cards.length).toBeGreaterThanOrEqual(1);
        expect(cards.some((c) => c.cardId === createdCardId)).toBe(true);
    });

    it("addBalance() → increases balance", async () => {
        const ok = await cardRepository.addBalance(createdCardId, 50);
        expect(ok).toBe(true);

        const card = await cardRepository.findById(createdCardId);
        expect(card!.balance).toBe(75); // 25 + 50
    });

    it("updateStatus() → freezes card", async () => {
        const ok = await cardRepository.updateStatus(createdCardId, "frozen");
        expect(ok).toBe(true);

        const card = await cardRepository.findById(createdCardId);
        expect(card!.status).toBe("frozen");
    });

    it("updateStatus() → unfreezes card", async () => {
        const ok = await cardRepository.updateStatus(createdCardId, "active");
        expect(ok).toBe(true);

        const card = await cardRepository.findById(createdCardId);
        expect(card!.status).toBe("active");
    });
});

// ── Payment Repository Tests ───────────────────────────────

describe("PaymentRepository", () => {
    const testTxHash = `tx_persist_test_${Date.now()}`;

    it("recordPayment() → stores payment", async () => {
        const { record: payment, inserted } = await paymentRepository.recordPayment({
            txHash: testTxHash,
            payer: "GPAYER111111111111111111111111111111111111111111111111111",
            amount: "25000000",
            tierAmount: 25 as TierAmount,
            status: "proof_received"
        });

        expect(inserted).toBe(true);
        expect(payment.id).toBeTruthy();
        expect(payment.txHash).toBe(testTxHash);
        expect(payment.status).toBe("proof_received");
    });

    it("findByTxHash() → returns existing payment", async () => {
        const payment = await paymentRepository.findByTxHash(testTxHash);
        expect(payment).toBeDefined();
        expect(payment!.txHash).toBe(testTxHash);
    });

    it("findByTxHash() → returns undefined for unknown hash", async () => {
        const payment = await paymentRepository.findByTxHash("tx_unknown_hash");
        expect(payment).toBeUndefined();
    });

    it("anti-replay: duplicate txHash returns existing record with inserted=false", async () => {
        const { record: duplicate, inserted } = await paymentRepository.recordPayment({
            txHash: testTxHash,
            payer: "GPAYER111111111111111111111111111111111111111111111111111",
            amount: "25000000",
            tierAmount: 25 as TierAmount,
            status: "verified"
        });

        expect(inserted).toBe(false);
        // Should return the ORIGINAL record with proof_received status
        expect(duplicate.txHash).toBe(testTxHash);
        expect(duplicate.status).toBe("proof_received");
    });

    it("concurrent anti-replay: exactly 1 inserted, rest duplicates", async () => {
        const concurrentHash = `tx_concurrent_${Date.now()}`;
        const basePayment = {
            txHash: concurrentHash,
            payer: "GPAYER111111111111111111111111111111111111111111111111111",
            amount: "50000000",
            tierAmount: 50 as TierAmount,
            status: "proof_received" as const
        };

        // Fire 5 concurrent inserts with the same txHash
        const results = await Promise.all([
            paymentRepository.recordPayment(basePayment),
            paymentRepository.recordPayment(basePayment),
            paymentRepository.recordPayment(basePayment),
            paymentRepository.recordPayment(basePayment),
            paymentRepository.recordPayment(basePayment)
        ]);

        // All should resolve to the same txHash
        const hashes = new Set(results.map((r) => r.record.txHash));
        expect(hashes.size).toBe(1);
        expect(hashes.has(concurrentHash)).toBe(true);

        // Exactly 1 inserted, rest are duplicates
        const insertedCount = results.filter((r) => r.inserted).length;
        const duplicateCount = results.filter((r) => !r.inserted).length;
        expect(insertedCount).toBe(1);
        expect(duplicateCount).toBe(4);
    });

    it("markSettled() → transitions to settled", async () => {
        const ok = await paymentRepository.markSettled(testTxHash, "settle_abc123");
        expect(ok).toBe(true);

        const payment = await paymentRepository.findByTxHash(testTxHash);
        expect(payment!.status).toBe("settled");
        expect(payment!.settleId).toBe("settle_abc123");
    });

    it("markFailed() → transitions to settle_failed", async () => {
        const failHash = `tx_fail_${Date.now()}`;
        await paymentRepository.recordPayment({
            txHash: failHash,
            payer: "GPAYER111111111111111111111111111111111111111111111111111",
            amount: "10000000",
            tierAmount: 10 as TierAmount,
            status: "verified"
        });

        const ok = await paymentRepository.markFailed(failHash, "settle_failed");
        expect(ok).toBe(true);

        const payment = await paymentRepository.findByTxHash(failHash);
        expect(payment!.status).toBe("settle_failed");
    });
});

// ── Webhook Event Repository Tests ─────────────────────────

describe("WebhookEventRepository", () => {
    const testKey = `evt_persist_test_${Date.now()}`;

    it("store() → persists webhook event", async () => {
        const { record: event, inserted } = await webhookEventRepository.store({
            idempotencyKey: testKey,
            eventType: "card.created",
            payload: { foo: "bar" }
        });

        expect(inserted).toBe(true);
        expect(event.id).toBeTruthy();
        expect(event.idempotencyKey).toBe(testKey);
        expect(event.eventType).toBe("card.created");
    });

    it("findByIdempotencyKey() → returns stored event", async () => {
        const event = await webhookEventRepository.findByIdempotencyKey(testKey);
        expect(event).toBeDefined();
        expect(event!.idempotencyKey).toBe(testKey);
    });

    it("findByIdempotencyKey() → returns undefined for unknown key", async () => {
        const event = await webhookEventRepository.findByIdempotencyKey("unknown_key");
        expect(event).toBeUndefined();
    });

    it("idempotency: duplicate key returns existing record with inserted=false", async () => {
        const { record: duplicate, inserted } = await webhookEventRepository.store({
            idempotencyKey: testKey,
            eventType: "card.funded",
            payload: { baz: "qux" }
        });

        expect(inserted).toBe(false);
        // Should return original with card.created type
        expect(duplicate.idempotencyKey).toBe(testKey);
        expect(duplicate.eventType).toBe("card.created");
    });

    it("concurrent idempotency: exactly 1 inserted, rest duplicates", async () => {
        const concurrentKey = `evt_concurrent_${Date.now()}`;
        const baseEvent = {
            idempotencyKey: concurrentKey,
            eventType: "card.transaction",
            payload: { amount: 42 }
        };

        // Fire 5 concurrent stores with the same idempotencyKey
        const results = await Promise.all([
            webhookEventRepository.store(baseEvent),
            webhookEventRepository.store(baseEvent),
            webhookEventRepository.store(baseEvent),
            webhookEventRepository.store(baseEvent),
            webhookEventRepository.store(baseEvent)
        ]);

        // All should resolve to the same key
        const keys = new Set(results.map((r) => r.record.idempotencyKey));
        expect(keys.size).toBe(1);
        expect(keys.has(concurrentKey)).toBe(true);

        // Exactly 1 inserted, rest are duplicates
        const insertedCount = results.filter((r) => r.inserted).length;
        const duplicateCount = results.filter((r) => !r.inserted).length;
        expect(insertedCount).toBe(1);
        expect(duplicateCount).toBe(4);
    });
});
