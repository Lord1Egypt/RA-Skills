import assert from "node:assert/strict";
import { createAIVideoClient } from "./aivideo-client.mjs";

const calls = [];
globalThis.fetch = async (url, init) => {
  calls.push({ url, init });

  if (url.includes("task_network_error")) {
    throw new Error("network unavailable");
  }

  if (init.method === "PUT") {
    if (url.endsWith("/task_cancellable/cancel")) {
      return new Response(JSON.stringify({ status: "CANCEL" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }
    return new Response(JSON.stringify({ status: "FAILED", error: "Task cannot be cancelled" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  if (init.method === "POST") {
    return new Response(JSON.stringify({ status: "SUBMITTED", taskId: "task_123" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ status: "PROGRESS" }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
};

const client = createAIVideoClient({
  apiKey: "test-key",
  baseUrl: "https://example.test",
  debug: false,
  maxRetries: 0,
});

const statusResult = await client.getStatus("task_123");
assert.equal(statusResult.ok, true);
assert.equal(statusResult.status, "PROGRESS");
assert.equal(statusResult.taskId, "task_123");
assert.equal(calls[0].init.headers.key, "test-key");
assert.equal(calls[0].init.headers["Content-Type"], undefined);

const createResult = await client.createGeneration({
  model: "t2v",
  payload: { prompt: "A sunrise", aspectRatio: "16:9", duration: "5" },
  maxCredits: 15,
});
assert.equal(createResult.ok, true);
assert.equal(calls[1].init.headers["Content-Type"], "application/json");

const cancelResult = await client.cancelTask("task_123");
assert.equal(cancelResult.ok, false);
assert.equal(cancelResult.errorMessage, "Task cannot be cancelled");
assert.equal(cancelResult.taskId, "task_123");

const successfulCancelResult = await client.cancelTask("task_cancellable");
assert.equal(successfulCancelResult.ok, true);
assert.equal(successfulCancelResult.status, "CANCEL");
assert.equal(successfulCancelResult.taskId, "task_cancellable");

const networkErrorResult = await client.getStatus("task_network_error");
assert.equal(networkErrorResult.ok, false);
assert.equal(networkErrorResult.errorCode, "NETWORK_ERROR");
assert.equal(networkErrorResult.taskId, "task_network_error");

console.log("Validated API client request and error handling.");
