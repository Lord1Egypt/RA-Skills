/**
 * Tests for lib/errors.js
 *
 * Covers: error class properties, fromResponse() HTTP mapping,
 * and the critical 503 split between platform-pause and payment-settlement.
 */

import { test } from "node:test"
import assert from "node:assert/strict"

import {
  ClabcrawError,
  PausedError,
  InsufficientFundsError,
  NotYourTurnError,
  InvalidActionError,
  GameNotFoundError,
  NetworkError,
  AuthError,
  GameDisabledError,
  fromResponse,
} from "../lib/errors.js"

// ─── Helpers ──────────────────────────────────────────────────────────────────

/**
 * Build a minimal fetch-like Response mock.
 */
function mockResponse(status, body = {}, headers = {}) {
  return {
    status,
    ok: status >= 200 && status < 300,
    statusText: `HTTP ${status}`,
    json: async () => body,
    headers: { get: (k) => headers[k.toLowerCase()] ?? null },
  }
}

// ─── Error class properties ───────────────────────────────────────────────────

test("ClabcrawError sets code, retriable, retryAfterMs, context", () => {
  const err = new ClabcrawError("oops", { code: "TEST", retriable: true, retryAfterMs: 1000, context: { x: 1 } })
  assert.equal(err.message, "oops")
  assert.equal(err.code, "TEST")
  assert.equal(err.retriable, true)
  assert.equal(err.retryAfterMs, 1000)
  assert.deepEqual(err.context, { x: 1 })
  assert.ok(err instanceof Error)
})

test("PausedError defaults: retriable=true, retryAfterMs=30000", () => {
  const err = new PausedError()
  assert.equal(err.code, "PAUSED")
  assert.equal(err.retriable, true)
  assert.equal(err.retryAfterMs, 30_000)
  assert.ok(err instanceof ClabcrawError)
})

test("PausedError accepts retriable=false override", () => {
  const err = new PausedError("paused", { retriable: false, retryAfterMs: 300_000 })
  assert.equal(err.retriable, false)
  assert.equal(err.retryAfterMs, 300_000)
})

test("InsufficientFundsError: not retriable", () => {
  const err = new InsufficientFundsError()
  assert.equal(err.code, "INSUFFICIENT_FUNDS")
  assert.equal(err.retriable, false)
})

test("NotYourTurnError: retriable, 1s delay", () => {
  const err = new NotYourTurnError()
  assert.equal(err.code, "NOT_YOUR_TURN")
  assert.equal(err.retriable, true)
  assert.equal(err.retryAfterMs, 1_000)
})

test("InvalidActionError: not retriable", () => {
  const err = new InvalidActionError()
  assert.equal(err.code, "INVALID_ACTION")
  assert.equal(err.retriable, false)
})

test("GameNotFoundError: not retriable, includes gameId in message", () => {
  const err = new GameNotFoundError("abc-123")
  assert.equal(err.code, "GAME_NOT_FOUND")
  assert.equal(err.retriable, false)
  assert.ok(err.message.includes("abc-123"))
})

test("NetworkError: retriable, 3s default delay", () => {
  const err = new NetworkError()
  assert.equal(err.code, "NETWORK_ERROR")
  assert.equal(err.retriable, true)
  assert.equal(err.retryAfterMs, 3_000)
})

test("AuthError: not retriable", () => {
  const err = new AuthError()
  assert.equal(err.code, "AUTH_ERROR")
  assert.equal(err.retriable, false)
})

test("GameDisabledError: not retriable, exposes availableGames", () => {
  const err = new GameDisabledError("disabled", { availableGames: ["poker-novice", "poker", "poker-pro"] })
  assert.equal(err.code, "GAME_DISABLED")
  assert.equal(err.retriable, false)
  assert.deepEqual(err.availableGames, ["poker-novice", "poker", "poker-pro"])
})

// ─── fromResponse: status code mapping ───────────────────────────────────────

test("fromResponse 400 with available_games → GameDisabledError", async () => {
  const res = mockResponse(400, { error: "Game disabled", available_games: ["poker"] })
  const err = await fromResponse(res)
  assert.ok(err instanceof GameDisabledError)
  assert.equal(err.code, "GAME_DISABLED")
  assert.deepEqual(err.availableGames, ["poker"])
})

test("fromResponse 400 without available_games → ClabcrawError BAD_REQUEST", async () => {
  const res = mockResponse(400, { error: "Bad request" })
  const err = await fromResponse(res)
  assert.ok(err instanceof ClabcrawError)
  assert.equal(err.code, "BAD_REQUEST")
  assert.equal(err.retriable, false)
})

test("fromResponse 401 → AuthError", async () => {
  const res = mockResponse(401, { error: "Unauthorized" })
  const err = await fromResponse(res)
  assert.ok(err instanceof AuthError)
  assert.equal(err.code, "AUTH_ERROR")
})

test("fromResponse 402 → InsufficientFundsError", async () => {
  const res = mockResponse(402, { error: "Payment required" })
  const err = await fromResponse(res)
  assert.ok(err instanceof InsufficientFundsError)
  assert.equal(err.code, "INSUFFICIENT_FUNDS")
})

test("fromResponse 404 → GameNotFoundError with provided gameId", async () => {
  const res = mockResponse(404, {})
  const err = await fromResponse(res, "game-xyz")
  assert.ok(err instanceof GameNotFoundError)
  assert.ok(err.message.includes("game-xyz"))
})

test("fromResponse 404 without gameId → GameNotFoundError with 'unknown'", async () => {
  const res = mockResponse(404, {})
  const err = await fromResponse(res)
  assert.ok(err instanceof GameNotFoundError)
  assert.ok(err.message.includes("unknown"))
})

test("fromResponse 422 → InvalidActionError", async () => {
  const res = mockResponse(422, { error: "Invalid action" })
  const err = await fromResponse(res)
  assert.ok(err instanceof InvalidActionError)
  assert.equal(err.code, "INVALID_ACTION")
})

// ─── 503 split: platform pause vs. payment settlement ─────────────────────────

test("fromResponse 503 without retryable → PausedError with retriable=false", async () => {
  const res = mockResponse(503, { error: "Platform is paused for maintenance" })
  const err = await fromResponse(res)
  assert.ok(err instanceof PausedError)
  assert.equal(err.code, "PAUSED")
  assert.equal(err.retriable, false, "platform pause must NOT auto-retry in _request")
})

test("fromResponse 503 with retryable=true → PausedError with retriable=true", async () => {
  const res = mockResponse(503, { retryable: true, error: "Payment settlement pending" })
  const err = await fromResponse(res)
  assert.ok(err instanceof PausedError)
  assert.equal(err.code, "PAUSED")
  assert.equal(err.retriable, true, "payment settlement SHOULD auto-retry in _request")
})

test("fromResponse 503 reads Retry-After header into retryAfterMs", async () => {
  const res = mockResponse(503, { error: "Paused" }, { "retry-after": "120" })
  const err = await fromResponse(res)
  assert.equal(err.retryAfterMs, 120_000)
})

test("fromResponse 503 with short Retry-After for settlement", async () => {
  const res = mockResponse(503, { retryable: true }, { "retry-after": "5" })
  const err = await fromResponse(res)
  assert.equal(err.retryAfterMs, 5_000)
  assert.equal(err.retriable, true)
})

// ─── fromResponse: 5xx fallback ───────────────────────────────────────────────

test("fromResponse 500 → ClabcrawError HTTP_ERROR, retriable=true", async () => {
  const res = mockResponse(500, { error: "Internal error" })
  const err = await fromResponse(res)
  assert.ok(err instanceof ClabcrawError)
  assert.equal(err.code, "HTTP_ERROR")
  assert.equal(err.retriable, true)
})

test("fromResponse 502 → ClabcrawError HTTP_ERROR, retriable=true", async () => {
  const res = mockResponse(502, {})
  const err = await fromResponse(res)
  assert.equal(err.code, "HTTP_ERROR")
  assert.equal(err.retriable, true)
})

test("fromResponse 400-range unknown → ClabcrawError HTTP_ERROR, retriable=false", async () => {
  const res = mockResponse(409, { error: "Conflict" })
  const err = await fromResponse(res)
  assert.equal(err.code, "HTTP_ERROR")
  assert.equal(err.retriable, false)
})

// ─── Retry-After header parsing ───────────────────────────────────────────────

test("fromResponse uses default retryAfterMs=5000 when no Retry-After header", async () => {
  const res = mockResponse(503, { retryable: true })
  const err = await fromResponse(res)
  assert.equal(err.retryAfterMs, 5_000)
})

test("fromResponse parses Retry-After as integer seconds", async () => {
  const res = mockResponse(503, {}, { "retry-after": "30" })
  const err = await fromResponse(res)
  assert.equal(err.retryAfterMs, 30_000)
})
