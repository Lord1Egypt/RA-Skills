import crypto from "node:crypto";
import http from "node:http";
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { createApp } from "../src/app";

const app = createApp();
const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET ?? "dev-placeholder-webhook-secret";

// ── Native HTTP helper for webhook tests ──────────────────
// supertest re-encodes Buffer bodies, breaking HMAC verification.
// We use native http.request to send bytes exactly as signed.

let server: http.Server;
let basePort: number;

beforeAll(async () => {
    await new Promise<void>((resolve) => {
        server = app.listen(0, () => {
            const addr = server.address() as { port: number };
            basePort = addr.port;
            resolve();
        });
    });
});

afterAll(async () => {
    await new Promise<void>((resolve) => {
        server.close(() => resolve());
    });
});

const postWebhook = (
    payload: string,
    headers: Record<string, string>
): Promise<{ status: number; body: Record<string, unknown> }> =>
    new Promise((resolve, reject) => {
        const options: http.RequestOptions = {
            hostname: "localhost",
            port: basePort,
            path: "/webhooks/4payments",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Content-Length": Buffer.byteLength(payload),
                ...headers
            }
        };
        const req = http.request(options, (res) => {
            let data = "";
            res.on("data", (chunk) => { data += chunk; });
            res.on("end", () => {
                resolve({
                    status: res.statusCode ?? 0,
                    body: JSON.parse(data)
                });
            });
        });
        req.on("error", reject);
        req.write(payload);
        req.end();
    });

const signPayload = (payload: string, secret: string): string =>
    crypto.createHmac("sha256", secret).update(payload).digest("hex");

// ── Webhook HMAC Tests ─────────────────────────────────────

describe("Webhook — HMAC Verification", () => {
    it("POST /webhooks/4payments with valid webhook-sign → 200", async () => {
        const payload = JSON.stringify({
            type: "card.created",
            id: "evt_hmac_001",
            data: { card_id: "card_test" }
        });
        const sig = signPayload(payload, WEBHOOK_SECRET);

        const res = await postWebhook(payload, { "webhook-sign": sig });

        expect(res.status).toBe(200);
        expect(res.body.status).toBe("accepted");
        expect(res.body.type).toBe("card.created");
    });

    it("POST /webhooks/4payments with X-Webhook-Signature (fallback) → 200", async () => {
        const payload = JSON.stringify({
            type: "card.funded",
            id: "evt_hmac_002",
            data: {}
        });
        const sig = signPayload(payload, WEBHOOK_SECRET);

        const res = await postWebhook(payload, { "X-Webhook-Signature": sig });

        expect(res.status).toBe(200);
        expect(res.body.status).toBe("accepted");
    });

    it("POST /webhooks/4payments with invalid signature → 401", async () => {
        const payload = JSON.stringify({ type: "test", id: "evt_hmac_003" });

        const res = await postWebhook(payload, { "webhook-sign": "deadbeef" });

        expect(res.status).toBe(401);
        expect(res.body.error).toBe("Invalid webhook signature");
    });

    it("POST /webhooks/4payments without signature header → 401", async () => {
        const payload = JSON.stringify({ type: "test", id: "evt_hmac_004" });

        const res = await postWebhook(payload, {});

        expect(res.status).toBe(401);
        expect((res.body.error as string)).toContain("Missing webhook signature");
    });

    it("POST /webhooks/4payments idempotency — duplicate event → already_processed", async () => {
        const payload = JSON.stringify({
            type: "card.status_change",
            id: "evt_idempotent_native_001",
            data: {}
        });
        const sig = signPayload(payload, WEBHOOK_SECRET);

        // First call
        const res1 = await postWebhook(payload, { "webhook-sign": sig });
        expect(res1.status).toBe(200);
        expect(res1.body.status).toBe("accepted");

        // Second call with same idempotency key
        const res2 = await postWebhook(payload, { "webhook-sign": sig });
        expect(res2.status).toBe(200);
        expect(res2.body.status).toBe("already_processed");
    });
});

// ── x402 Fail-Closed Test (uses supertest — fine for JSON routes) ──

describe("x402 Verify — Fail-Closed", () => {
    it("POST /cards/create/tier/25 with bogus X-Payment → rejected (401 or 503)", async () => {
        const payment = {
            scheme: "exact",
            network: "stellar:pubnet",
            payload: {
                txHash: "abc123valid",
                authorization: {
                    from: process.env.STELLAR_TREASURY_ADDRESS,
                    to: process.env.STELLAR_TREASURY_ADDRESS,
                    value: "32500000"
                }
            }
        };
        const encoded = Buffer.from(JSON.stringify(payment)).toString("base64");

        const res = await request(app)
            .post("/cards/create/tier/25")
            .set("X-Payment", encoded);

        // Fail-closed: facilitator rejects bogus tx (401) or is unreachable (503).
        // Either way the request MUST NOT proceed to the paid handler.
        expect([401, 503]).toContain(res.status);
        expect(res.body.error).toBeDefined();
    });
});
