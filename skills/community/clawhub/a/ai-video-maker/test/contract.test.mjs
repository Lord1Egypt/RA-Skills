import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import test from "node:test";

import { ALLOWED_MODELS, validateCreatePayload } from "../scripts/contract.mjs";

const validPayloads = {
  t2v: { prompt: "A sunrise", aspectRatio: "16:9", duration: "5" },
  i2v: { image: "https://example.com/frame.jpg", prompt: null, duration: "5" },
  minimax: {
    content: "A cinematic candle",
    duration: 5,
    resolution: "720p",
    tier: "turbo",
    aspectRatio: "16:9",
  },
  t2v_v3: { prompt: "A sunrise", aspectRatio: "16:9", duration: "10" },
  i2v_v3: {
    image: "data:image/png;base64,YQ==",
    prompt: "Move slowly",
    duration: "10",
  },
  seedance20: { prompt: "A sunrise", duration: 5, resolution: 720, ratio: "16:9" },
  wan30: {
    prompt: "A sunrise",
    duration: "5",
    resolution: "480P",
    ratio: "16:9",
  },
  happyhorse: {
    prompt: "A horse running",
    duration: 5,
    resolution: "720P",
    ratio: "16:9",
  },
};

test("every advertised model has a working contract", () => {
  assert.deepEqual(ALLOWED_MODELS, Object.keys(validPayloads));
  for (const [model, payload] of Object.entries(validPayloads)) {
    assert.deepEqual(validateCreatePayload(model, payload), { ok: true }, model);
  }
});

test("MiniMax validates its numeric duration independently", () => {
  const invalid = validateCreatePayload("minimax", {
    content: "A cinematic candle",
    duration: "5",
    resolution: "720p",
    tier: "turbo",
  });
  assert.equal(invalid.ok, false);
  assert.equal(
    invalid.details.some((detail) => detail.field === "duration"),
    true,
  );
});

test("MiniMax rejects mixed frame and reference modes", () => {
  const invalid = validateCreatePayload("minimax", {
    content: "Animate this",
    imageUrl: "https://example.com/frame.jpg",
    referenceVideoUrl: "https://example.com/reference.mp4",
  });
  assert.equal(invalid.ok, false);
  assert.equal(
    invalid.details.some((detail) => detail.field === "media"),
    true,
  );
});

test("advertised non-H3 models reject malformed payloads before billing", () => {
  assert.equal(
    validateCreatePayload("seedance20", { audio: "https://example.com/a.mp3" }).ok,
    false,
  );
  assert.equal(validateCreatePayload("wan30", { prompt: "", duration: 5 }).ok, false);
  assert.equal(validateCreatePayload("wan27", { prompt: "A sunrise", duration: "5" }).ok, false);
  assert.equal(
    validateCreatePayload("happyhorse", {
      prompt: "Horse",
      duration: 5,
      resolution: "480P",
    }).ok,
    false,
  );
});

test("validation failures return JSON and a nonzero process exit", () => {
  const result = spawnSync(
    process.execPath,
    [
      "scripts/run-workflow.mjs",
      "--model",
      "minimax",
      "--payload",
      JSON.stringify({ content: "Test", duration: "5" }),
      "--maxCredits",
      "15",
    ],
    {
      cwd: new URL("..", import.meta.url),
      env: { ...process.env, AIVIDEO_API_KEY: "test-key" },
      encoding: "utf8",
    },
  );

  assert.equal(result.status, 1);
  assert.equal(result.stderr, "");
  assert.equal(JSON.parse(result.stdout).errorCode, "INVALID_PAYLOAD");
});

test("polling timeout exits 2 and preserves the resumable task ID", () => {
  const result = spawnSync(
    process.execPath,
    [
      "--import",
      "./test/mock-fetch.mjs",
      "scripts/run-workflow.mjs",
      "--model",
      "minimax",
      "--payload",
      JSON.stringify({ content: "Test", duration: 5 }),
      "--maxCredits",
      "15",
      "--maxWaitMs",
      "1",
      "--pollMinMs",
      "1",
    ],
    {
      cwd: new URL("..", import.meta.url),
      env: {
        ...process.env,
        AIVIDEO_API_KEY: "test-key",
        AIVIDEO_MAX_RETRIES: "0",
        AIVIDEO_TEST_SCENARIO: "timeout",
      },
      encoding: "utf8",
    },
  );

  const output = JSON.parse(result.stdout);
  assert.equal(result.status, 2);
  assert.equal(output.errorCode, "POLL_TIMEOUT");
  assert.equal(output.taskId, "task-resumable");
});

test("terminal generation failure exits 1", () => {
  const result = spawnSync(
    process.execPath,
    [
      "--import",
      "./test/mock-fetch.mjs",
      "scripts/run-workflow.mjs",
      "--model",
      "minimax",
      "--payload",
      JSON.stringify({ content: "Test", duration: 5 }),
      "--maxCredits",
      "15",
    ],
    {
      cwd: new URL("..", import.meta.url),
      env: {
        ...process.env,
        AIVIDEO_API_KEY: "test-key",
        AIVIDEO_MAX_RETRIES: "0",
        AIVIDEO_TEST_SCENARIO: "failed",
      },
      encoding: "utf8",
    },
  );

  const output = JSON.parse(result.stdout);
  assert.equal(result.status, 1);
  assert.equal(output.status, "FAILED");
  assert.equal(output.taskId, "task-resumable");
});
