import { describe, it, expect } from "vitest";
import request from "supertest";
import { createApp } from "../src/app";

const app = createApp();

describe("x402 Challenge — Create Tiers", () => {
    const createTiers = [10, 25, 50, 100, 200, 500] as const;
    const expectedAtomicAmounts: Record<number, string> = {
        10: "17200000",   // totalCost = 17.2
        25: "32500000",   // totalCost = 32.5
        50: "58000000",   // totalCost = 58.0
        100: "110000000", // totalCost = 110.0
        200: "214000000", // totalCost = 214.0
        500: "522000000"  // totalCost = 522.0
    };

    for (const amount of createTiers) {
        it(`POST /cards/create/tier/${amount} → 402 with correct challenge`, async () => {
            const res = await request(app)
                .post(`/cards/create/tier/${amount}`)
                .expect(402);

            expect(res.body).toHaveProperty("x402Version", 2);
            expect(res.body.accepts).toHaveLength(1);

            const accept = res.body.accepts[0];
            expect(accept.scheme).toBe("exact");
            expect(accept.network).toBe("stellar:pubnet");
            expect(accept.asset).toContain("USDC:");
            expect(accept.asset).toContain("GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN");
            expect(accept.amount).toBe(expectedAtomicAmounts[amount]);
            expect(accept.payTo).toMatch(/^G[A-Z2-7]{55}$/);
            expect(accept.maxTimeoutSeconds).toBe(300);
            expect(res.body.resource.url).toContain(`/cards/create/tier/${amount}`);
            expect(res.body.resource.description).toContain(`$${amount}`);
        });
    }
});

describe("x402 Challenge — Fund Tiers", () => {
    const fundTiers = [10, 25, 50, 100, 200, 500] as const;
    const expectedAtomicAmounts: Record<number, string> = {
        10: "14200000",   // totalCost = 14.2
        25: "29500000",   // totalCost = 29.5
        50: "55000000",   // totalCost = 55.0
        100: "107000000", // totalCost = 107.0
        200: "211000000", // totalCost = 211.0
        500: "519000000"  // totalCost = 519.0
    };

    for (const amount of fundTiers) {
        it(`POST /cards/fund/tier/${amount} → 402 with correct challenge`, async () => {
            const res = await request(app)
                .post(`/cards/fund/tier/${amount}`)
                .expect(402);

            expect(res.body).toHaveProperty("x402Version", 2);
            expect(res.body.accepts[0].amount).toBe(expectedAtomicAmounts[amount]);
            expect(res.body.resource.url).toContain(`/cards/fund/tier/${amount}`);
        });
    }
});

describe("x402 Challenge — Error Cases", () => {
    it("POST /cards/create/tier/999 → 400 (unsupported tier)", async () => {
        const res = await request(app)
            .post("/cards/create/tier/999")
            .expect(400);

        expect(res.body.error).toBe("Unsupported tier amount");
    });

    it("POST /cards/fund/tier/42 → 400 (unsupported tier)", async () => {
        const res = await request(app)
            .post("/cards/fund/tier/42")
            .expect(400);

        expect(res.body.error).toBe("Unsupported tier amount");
    });

    it("POST /cards/create/tier/25 with malformed X-Payment → 401", async () => {
        const res = await request(app)
            .post("/cards/create/tier/25")
            .set("X-Payment", "not-valid-json-or-base64")
            .expect(401);

        expect(res.body.error).toBe("Invalid X-PAYMENT header: expected x402 v2 PaymentPayload");
    });

    it("POST /cards/create/tier/25 with wrong network in X-Payment → 401", async () => {
        const payment = {
            x402Version: 2,
            accepted: {
                scheme: "exact",
                network: "eip155:1" // wrong network
            },
            payload: {
                transaction: "xyz"
            }
        };
        const encoded = Buffer.from(JSON.stringify(payment)).toString("base64");
        const res = await request(app)
            .post("/cards/create/tier/25")
            .set("X-Payment", encoded)
            .expect(401);

        expect(res.body.error).toBe("Unsupported payment scheme or network");
    });
});

describe("Public Endpoints", () => {
    it("GET /health → 200 with status ok", async () => {
        const res = await request(app)
            .get("/health")
            .expect(200);

        expect(res.body.status).toBe("ok");
        expect(res.body.version).toBeDefined();
        expect(res.body.timestamp).toBeDefined();
    });

    it("GET /pricing → 200 with 6 creation + 6 funding tiers", async () => {
        const res = await request(app)
            .get("/pricing")
            .expect(200);

        expect(res.body.creation.tiers).toHaveLength(6);
        expect(res.body.funding.tiers).toHaveLength(6);
    });

    it("GET /cards/tiers → 200 with breakdown", async () => {
        const res = await request(app)
            .get("/cards/tiers")
            .expect(200);

        expect(res.body.creation).toBeDefined();
        expect(res.body.creation[0].breakdown).toBeDefined();
    });

    it("GET /nonexistent → 404", async () => {
        await request(app)
            .get("/nonexistent")
            .expect(404);
    });
});

describe("Wallet Auth Errors", () => {
    it("GET /wallet → 401 without auth headers", async () => {
        const res = await request(app)
            .get("/cards")
            .expect(401);

        expect(res.body.error).toBe("Missing wallet authentication headers");
    });

    it("GET /wallet → 401 with invalid timestamp", async () => {
        const res = await request(app)
            .get("/cards")
            .set("X-WALLET-ADDRESS", "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            .set("X-WALLET-SIGNATURE", "dGVzdA==")
            .set("X-WALLET-TIMESTAMP", "not-a-number")
            .expect(401);

        expect(res.body.error).toBe("Invalid wallet timestamp");
    });

    it("GET /wallet → 401 with expired timestamp", async () => {
        const oldTimestamp = Math.floor(Date.now() / 1000) - 600;
        const res = await request(app)
            .get("/cards")
            .set("X-WALLET-ADDRESS", "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            .set("X-WALLET-SIGNATURE", "dGVzdA==")
            .set("X-WALLET-TIMESTAMP", String(oldTimestamp))
            .expect(401);

        expect(res.body.error).toBe("Wallet timestamp outside accepted window");
    });
});
