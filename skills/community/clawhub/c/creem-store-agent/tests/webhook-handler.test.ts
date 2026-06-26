import { describe, it, expect, vi, beforeEach } from "vitest";
import { createHmac } from "node:crypto";
import { Readable } from "node:stream";
import { createWebhookHandler, verifySignature } from "../src/webhook-handler";
import type { CreemWebhookPayload } from "../src/types";

function createMockReq(body: string, headers: Record<string, string> = {}): any {
  const readable = Readable.from([Buffer.from(body)]);
  (readable as any).headers = {};
  for (const [key, value] of Object.entries(headers)) {
    (readable as any).headers[key.toLowerCase()] = value;
  }
  return readable;
}

function createMockRes(): any {
  const res: any = {
    statusCode: 200,
    writeHead: vi.fn().mockReturnThis(),
    end: vi.fn(),
    setHeader: vi.fn(),
  };
  return res;
}

function signBody(body: string, secret: string): string {
  return createHmac("sha256", secret).update(body).digest("hex");
}

const TEST_SECRET = "whsec_test_secret_123";

describe("verifySignature", () => {
  it("returns true for valid HMAC-SHA256 signature", () => {
    const body = '{"eventType":"checkout.completed","id":"evt_1","created_at":1742198400,"object":{}}';
    const signature = signBody(body, TEST_SECRET);
    expect(verifySignature(body, signature, TEST_SECRET)).toBe(true);
  });

  it("returns false for invalid signature", () => {
    const body = '{"eventType":"checkout.completed"}';
    expect(verifySignature(body, "invalid_hex", TEST_SECRET)).toBe(false);
  });

  it("returns false for empty signature", () => {
    const body = '{"test": true}';
    expect(verifySignature(body, "", TEST_SECRET)).toBe(false);
  });

  it("returns false for tampered body", () => {
    const body = '{"eventType":"checkout.completed"}';
    const signature = signBody(body, TEST_SECRET);
    const tampered = '{"eventType":"dispute.created"}';
    expect(verifySignature(tampered, signature, TEST_SECRET)).toBe(false);
  });

  it("returns false for wrong secret", () => {
    const body = '{"test": true}';
    const signature = signBody(body, TEST_SECRET);
    expect(verifySignature(body, signature, "wrong_secret")).toBe(false);
  });
});

describe("createWebhookHandler", () => {
  let onEvent: any;

  beforeEach(() => {
    onEvent = vi.fn();
  });

  it("returns 401 when creem-signature header is missing", async () => {
    const handler = createWebhookHandler({ secret: TEST_SECRET, onEvent });
    const body = '{"eventType":"checkout.completed","id":"evt_1","created_at":1742198400,"object":{}}';
    const req = createMockReq(body, {});
    const res = createMockRes();

    const result = await handler(req, res);

    expect(res.writeHead).toHaveBeenCalledWith(401, expect.objectContaining({ "Content-Type": "application/json" }));
    expect(res.end).toHaveBeenCalledWith(expect.stringContaining("Missing signature"));
    expect(result).toBe(true);
    expect(onEvent).not.toHaveBeenCalled();
  });

  it("returns 401 when signature is invalid", async () => {
    const handler = createWebhookHandler({ secret: TEST_SECRET, onEvent });
    const body = '{"eventType":"checkout.completed","id":"evt_1","created_at":1742198400,"object":{}}';
    const req = createMockReq(body, { "creem-signature": "bad_sig" });
    const res = createMockRes();

    const result = await handler(req, res);

    expect(res.writeHead).toHaveBeenCalledWith(401, expect.objectContaining({ "Content-Type": "application/json" }));
    expect(res.end).toHaveBeenCalledWith(expect.stringContaining("Invalid signature"));
    expect(result).toBe(true);
    expect(onEvent).not.toHaveBeenCalled();
  });

  it("returns 200 and calls onEvent for valid request", async () => {
    const handler = createWebhookHandler({ secret: TEST_SECRET, onEvent });
    const payload: CreemWebhookPayload = {
      eventType: "checkout.completed",
      id: "evt_valid_1",
      created_at: 1742198400,
      object: { amount: 4900 },
    };
    const body = JSON.stringify(payload);
    const signature = signBody(body, TEST_SECRET);
    const req = createMockReq(body, { "creem-signature": signature });
    const res = createMockRes();

    const result = await handler(req, res);

    expect(res.writeHead).toHaveBeenCalledWith(200, expect.objectContaining({ "Content-Type": "application/json" }));
    expect(res.end).toHaveBeenCalledWith(expect.stringContaining("ok"));
    expect(result).toBe(true);
    expect(onEvent).toHaveBeenCalledWith(payload);
  });

  it("deduplicates events by id (returns 200 but does not call onEvent twice)", async () => {
    const handler = createWebhookHandler({ secret: TEST_SECRET, onEvent });
    const payload: CreemWebhookPayload = {
      eventType: "subscription.active",
      id: "evt_dedup_1",
      created_at: 1742198400,
      object: {},
    };
    const body = JSON.stringify(payload);
    const signature = signBody(body, TEST_SECRET);

    const req1 = createMockReq(body, { "creem-signature": signature });
    const res1 = createMockRes();
    await handler(req1, res1);

    const req2 = createMockReq(body, { "creem-signature": signature });
    const res2 = createMockRes();
    const result = await handler(req2, res2);

    expect(res2.writeHead).toHaveBeenCalledWith(200, expect.any(Object));
    expect(result).toBe(true);
    expect(onEvent).toHaveBeenCalledTimes(1);
  });

  it("returns 400 for unparseable JSON body", async () => {
    const handler = createWebhookHandler({ secret: TEST_SECRET, onEvent });
    const body = "not json";
    const signature = signBody(body, TEST_SECRET);
    const req = createMockReq(body, { "creem-signature": signature });
    const res = createMockRes();

    const result = await handler(req, res);

    expect(res.writeHead).toHaveBeenCalledWith(400, expect.any(Object));
    expect(result).toBe(true);
    expect(onEvent).not.toHaveBeenCalled();
  });

  it("handler always returns true (signals handled to OpenClaw)", async () => {
    const handler = createWebhookHandler({ secret: TEST_SECRET, onEvent });
    const body = '{}';
    const signature = signBody(body, TEST_SECRET);
    const req = createMockReq(body, { "creem-signature": signature });
    const res = createMockRes();

    const result = await handler(req, res);
    expect(result).toBe(true);
  });
});
