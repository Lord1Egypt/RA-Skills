/**
 * Tests for lib/schema.js
 *
 * Covers: parseCard() string parsing, normalizeState() field mapping,
 * action normalization, and edge cases (null input, unchanged flag, finished games).
 */

import { test } from "node:test"
import assert from "node:assert/strict"

import { parseCard, normalizeState } from "../lib/schema.js"

// ─── parseCard ────────────────────────────────────────────────────────────────

test("parseCard: standard rank + suit string", () => {
  assert.deepEqual(parseCard("Aspades"), { rank: "A", suit: "spades" })
  assert.deepEqual(parseCard("Khearts"), { rank: "K", suit: "hearts" })
  assert.deepEqual(parseCard("2clubs"), { rank: "2", suit: "clubs" })
  assert.deepEqual(parseCard("Tdiamonds"), { rank: "T", suit: "diamonds" })
})

test("parseCard: '10' two-character rank prefix", () => {
  assert.deepEqual(parseCard("10spades"), { rank: "10", suit: "spades" })
  assert.deepEqual(parseCard("10hearts"), { rank: "10", suit: "hearts" })
})

test("parseCard: already-parsed object passes through", () => {
  const card = { rank: "Q", suit: "clubs" }
  assert.equal(parseCard(card), card)
})

test("parseCard: invalid input returns unknown card", () => {
  assert.deepEqual(parseCard(""), { rank: "?", suit: "?" })
  assert.deepEqual(parseCard("X"), { rank: "?", suit: "?" })
  assert.deepEqual(parseCard(null), { rank: "?", suit: "?" })
  assert.deepEqual(parseCard(42), { rank: "?", suit: "?" })
})

// ─── normalizeState: edge cases ───────────────────────────────────────────────

test("normalizeState: null input returns unchanged sentinel", () => {
  const state = normalizeState(null)
  assert.equal(state.unchanged, true)
})

test("normalizeState: raw.unchanged=true returns unchanged sentinel", () => {
  const state = normalizeState({ unchanged: true })
  assert.equal(state.unchanged, true)
})

// ─── normalizeState: field mapping ───────────────────────────────────────────

const RAW_STATE = {
  game_id: "game-abc",
  hand_number: 3,
  current_street: "flop",
  is_your_turn: true,
  your_cards: ["Aspades", "Khearts"],
  community_cards: ["Tclubs", "7diamonds", "2hearts"],
  pot: 1200,
  your_stack: 8500,
  opponent_stack: 11500,
  move_deadline: new Date(Date.now() + 10_000).toISOString(),
  valid_actions: {
    fold: {},
    call: { amount: 100 },
    raise: { min: 200, max: 5000 },
  },
}

test("normalizeState: camelCase field names", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(state.gameId, "game-abc")
  assert.equal(state.handNumber, 3)
  assert.equal(state.street, "flop")
  assert.equal(state.isYourTurn, true)
  assert.equal(state.pot, 1200)
  assert.equal(state.yourStack, 8500)
  assert.equal(state.opponentStack, 11500)
  assert.equal(state.unchanged, false)
  assert.equal(state.isFinished, false)
})

test("normalizeState: hole cards parsed as objects", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(state.hole.length, 2)
  assert.deepEqual(state.hole[0], { rank: "A", suit: "spades" })
  assert.deepEqual(state.hole[1], { rank: "K", suit: "hearts" })
})

test("normalizeState: board cards parsed as objects", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(state.board.length, 3)
  assert.deepEqual(state.board[0], { rank: "T", suit: "clubs" })
  assert.deepEqual(state.board[1], { rank: "7", suit: "diamonds" })
  assert.deepEqual(state.board[2], { rank: "2", suit: "hearts" })
})

test("normalizeState: moveDeadlineMs is a number", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(typeof state.moveDeadlineMs, "number")
  // ~10 seconds in the future, allow 2s drift
  assert.ok(state.moveDeadlineMs > 8_000 && state.moveDeadlineMs < 12_000)
})

test("normalizeState: raw response preserved on state.raw", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(state.raw, RAW_STATE)
})

// ─── normalizeState: action normalization ────────────────────────────────────

test("normalizeState: present actions have available=true with details", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(state.actions.fold.available, true)
  assert.equal(state.actions.call.available, true)
  assert.equal(state.actions.call.amount, 100)
  assert.equal(state.actions.raise.available, true)
  assert.equal(state.actions.raise.min, 200)
  assert.equal(state.actions.raise.max, 5000)
})

test("normalizeState: absent actions have available=false", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(state.actions.check.available, false)
  assert.equal(state.actions.all_in.available, false)
})

test("normalizeState: all five action keys always present", () => {
  const state = normalizeState({ ...RAW_STATE, valid_actions: {} })
  const keys = Object.keys(state.actions)
  assert.ok(keys.includes("fold"))
  assert.ok(keys.includes("check"))
  assert.ok(keys.includes("call"))
  assert.ok(keys.includes("raise"))
  assert.ok(keys.includes("all_in"))
})

// ─── normalizeState: finished game ───────────────────────────────────────────

test("normalizeState: game_status=finished → isFinished=true, result set", () => {
  const raw = {
    ...RAW_STATE,
    game_status: "finished",
    result: "win",
    outcome: "knockout",
  }
  const state = normalizeState(raw)
  assert.equal(state.isFinished, true)
  assert.equal(state.result, "win")
  assert.equal(state.outcome, "knockout")
})

test("normalizeState: showdown includes opponent cards and winning hand", () => {
  const raw = {
    ...RAW_STATE,
    game_status: "finished",
    result: "loss",
    opponent_cards: ["Qspades", "Jhearts"],
    winning_hand: "Straight",
  }
  const state = normalizeState(raw)
  assert.equal(state.winningHand, "Straight")
  assert.ok(Array.isArray(state.opponentCards))
  assert.equal(state.opponentCards.length, 2)
  assert.deepEqual(state.opponentCards[0], { rank: "Q", suit: "spades" })
})

test("normalizeState: opponent_cards absent → opponentCards=null", () => {
  const state = normalizeState(RAW_STATE)
  assert.equal(state.opponentCards, null)
})

// ─── normalizeState: convenience fields ──────────────────────────────────────

test("normalizeState: potOdds computed from call amount and pot", () => {
  // call: 100, pot: 1200 → 100 / (1200 + 100) ≈ 0.0769
  const state = normalizeState(RAW_STATE)
  const expected = 100 / (1200 + 100)
  assert.ok(Math.abs(state.potOdds - expected) < 0.001, `potOdds ${state.potOdds} ≠ ${expected}`)
})

test("normalizeState: potOdds is 0 when no call action", () => {
  const raw = { ...RAW_STATE, valid_actions: { check: {}, fold: {} } }
  const state = normalizeState(raw)
  assert.equal(state.potOdds, 0)
})

test("normalizeState: effectiveStack is the smaller of the two stacks", () => {
  // your_stack: 8500, opponent_stack: 11500 → min = 8500
  const state = normalizeState(RAW_STATE)
  assert.equal(state.effectiveStack, 8500)
})

test("normalizeState: effectiveStack when opponent has fewer chips", () => {
  const raw = { ...RAW_STATE, your_stack: 15000, opponent_stack: 3000 }
  const state = normalizeState(raw)
  assert.equal(state.effectiveStack, 3000)
})

// ─── normalizeState: default values ─────────────────────────────────────────

test("normalizeState: missing optional fields default safely", () => {
  const state = normalizeState({ game_id: "x" })
  assert.equal(state.handNumber, 1)
  assert.equal(state.street, "preflop")
  assert.equal(state.isYourTurn, false)
  assert.equal(state.pot, 0)
  assert.equal(state.yourStack, 0)
  assert.equal(state.opponentStack, 0)
  assert.deepEqual(state.hole, [])
  assert.deepEqual(state.board, [])
  assert.equal(state.moveDeadlineMs, null)
  assert.equal(state.result, null)
  assert.equal(state.outcome, null)
})
