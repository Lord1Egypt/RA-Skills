import assert from "node:assert/strict";
import test from "node:test";

import { createAIVideoClient } from "../scripts/aivideo-client.mjs";

function jsonResponse(data, init = {}) {
  return new Response(JSON.stringify(data), {
    status: init.status ?? 200,
    headers: { "content-type": "application/json", ...(init.headers ?? {}) },
  });
}

test("HTTP 200 with terminal FAILED is not reported as success", async (t) => {
  t.mock.method(globalThis, "fetch", async () =>
    jsonResponse({ status: "FAILED", error: "Provider rejected the generation" }),
  );
  const client = createAIVideoClient({ apiKey: "test-key", debug: false });

  const result = await client.getStatus("task-123");
  assert.equal(result.ok, false);
  assert.equal(result.status, "FAILED");
  assert.equal(result.taskId, "task-123");
  assert.equal(result.errorMessage, "Provider rejected the generation");
});

test("read failures retain the task ID for safe resumption", async (t) => {
  t.mock.method(globalThis, "fetch", async () =>
    jsonResponse({ error: "Too many requests" }, { status: 429 }),
  );
  const client = createAIVideoClient({
    apiKey: "test-key",
    debug: false,
    maxRetries: 0,
  });

  const result = await client.getTask("task-456");
  assert.equal(result.ok, false);
  assert.equal(result.errorCode, "RATE_LIMITED");
  assert.equal(result.taskId, "task-456");
});

test("paid create requests retry safely with one stable idempotency key", async (t) => {
  let calls = 0;
  const idempotencyKeys = new Set();
  t.mock.method(globalThis, "fetch", async (_url, init) => {
    calls += 1;
    idempotencyKeys.add(init?.headers?.["Idempotency-Key"]);
    return jsonResponse({ message: "Temporary upstream failure" }, { status: 503 });
  });
  const client = createAIVideoClient({ apiKey: "test-key", debug: false, maxRetries: 3 });

  const result = await client.createGeneration({
    model: "minimax",
    payload: { content: "Test", duration: 5, resolution: "720p", tier: "turbo" },
    maxCredits: 15,
  });
  assert.equal(result.ok, false);
  assert.equal(calls, 4);
  assert.equal(idempotencyKeys.size, 1);
});

test("quote requests are non-billable and return the server price", async (t) => {
  t.mock.method(globalThis, "fetch", async (url) => {
    assert.match(String(url), /\/api\/v1\/quote\/minimax$/);
    return jsonResponse({ credits: 15, listPriceUsd: 0.15, billable: false });
  });
  const client = createAIVideoClient({ apiKey: "test-key", debug: false });
  const result = await client.quoteGeneration({
    model: "minimax",
    payload: { content: "Test", duration: 5, resolution: "720p", tier: "turbo" },
  });
  assert.equal(result.ok, true);
  assert.equal(result.data.credits, 15);
  assert.equal(result.data.billable, false);
});

test("a successful create response must include a task ID", async (t) => {
  t.mock.method(globalThis, "fetch", async () => jsonResponse({ status: "SUBMITTED" }));
  const client = createAIVideoClient({ apiKey: "test-key", debug: false });

  const result = await client.createGeneration({
    model: "minimax",
    payload: { content: "Test", duration: 5, resolution: "720p", tier: "turbo" },
    maxCredits: 15,
  });
  assert.equal(result.ok, false);
  assert.equal(result.errorCode, "INVALID_RESPONSE");
  assert.equal(typeof result.idempotencyKey, "string");
  assert.ok(result.idempotencyKey.length >= 8);
});
