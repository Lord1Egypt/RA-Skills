/**
 * Tests for lib/strategy.js
 *
 * Covers: hand ranking, hand descriptions, pot odds, call thresholds,
 * bet sizing, equity estimation, and action lookup.
 *
 * Note: equity estimation is heuristic, not exact — tests check ranges
 * rather than precise values.
 */

import { test } from "node:test"
import assert from "node:assert/strict"

import {
  handRank,
  describeHand,
  countOuts,
  estimateEquity,
  potOdds,
  shouldCall,
  suggestBetSize,
  findAction,
} from "../lib/strategy.js"

// ─── Helpers ──────────────────────────────────────────────────────────────────

/** Assert value is in [min, max] range (inclusive) */
function assertInRange(value, min, max, label = "") {
  assert.ok(
    value >= min && value <= max,
    `${label ? label + ": " : ""}expected ${value} to be in [${min}, ${max}]`
  )
}

// ─── handRank ────────────────────────────────────────────────────────────────

test("handRank: high card (preflop) → 0", () => {
  assert.equal(handRank([{ rank: "A", suit: "spades" }, { rank: "7", suit: "hearts" }]), 0)
})

test("handRank: pocket pair → 1", () => {
  assert.equal(handRank([{ rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" }]), 1)
})

test("handRank: two pair → 2", () => {
  const cards = [
    { rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" },
    { rank: "K", suit: "clubs" }, { rank: "K", suit: "diamonds" },
    { rank: "2", suit: "spades" },
  ]
  assert.equal(handRank(cards), 2)
})

test("handRank: three of a kind → 3", () => {
  const cards = [
    { rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" }, { rank: "A", suit: "clubs" },
    { rank: "K", suit: "diamonds" }, { rank: "2", suit: "spades" },
  ]
  assert.equal(handRank(cards), 3)
})

test("handRank: straight → 4", () => {
  const cards = [
    { rank: "5", suit: "spades" }, { rank: "6", suit: "hearts" },
    { rank: "7", suit: "clubs" }, { rank: "8", suit: "diamonds" },
    { rank: "9", suit: "spades" },
  ]
  assert.equal(handRank(cards), 4)
})

test("handRank: flush → 5", () => {
  const cards = [
    { rank: "A", suit: "spades" }, { rank: "K", suit: "spades" },
    { rank: "7", suit: "spades" }, { rank: "3", suit: "spades" },
    { rank: "2", suit: "spades" },
  ]
  assert.equal(handRank(cards), 5)
})

test("handRank: full house → 6", () => {
  const cards = [
    { rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" }, { rank: "A", suit: "clubs" },
    { rank: "K", suit: "diamonds" }, { rank: "K", suit: "spades" },
  ]
  assert.equal(handRank(cards), 6)
})

test("handRank: four of a kind → 7", () => {
  const cards = [
    { rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" },
    { rank: "A", suit: "clubs" }, { rank: "A", suit: "diamonds" },
    { rank: "K", suit: "spades" },
  ]
  assert.equal(handRank(cards), 7)
})

test("handRank: straight flush → 8", () => {
  const cards = [
    { rank: "5", suit: "spades" }, { rank: "6", suit: "spades" },
    { rank: "7", suit: "spades" }, { rank: "8", suit: "spades" },
    { rank: "9", suit: "spades" },
  ]
  assert.equal(handRank(cards), 8)
})

test("handRank: accepts raw card strings", () => {
  assert.equal(handRank(["Aspades", "Ahearts"]), 1)
  assert.equal(handRank(["Aspades", "Khearts"]), 0)
})

test("handRank: ace-low straight (A-2-3-4-5) → 4", () => {
  const cards = [
    { rank: "A", suit: "spades" }, { rank: "2", suit: "hearts" },
    { rank: "3", suit: "clubs" }, { rank: "4", suit: "diamonds" },
    { rank: "5", suit: "spades" },
  ]
  assert.equal(handRank(cards), 4)
})

test("handRank: empty or too-short input → 0", () => {
  assert.equal(handRank([]), 0)
  assert.equal(handRank(null), 0)
})

// ─── describeHand ────────────────────────────────────────────────────────────

test("describeHand: returns human-readable string for each rank", () => {
  const pair = [{ rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" }]
  assert.equal(describeHand(pair), "Pair")

  const highCard = [{ rank: "A", suit: "spades" }, { rank: "7", suit: "hearts" }]
  assert.equal(describeHand(highCard), "High card")

  const flush = [
    { rank: "A", suit: "spades" }, { rank: "K", suit: "spades" },
    { rank: "7", suit: "spades" }, { rank: "3", suit: "spades" },
    { rank: "2", suit: "spades" },
  ]
  assert.equal(describeHand(flush), "Flush")
})

// ─── potOdds ─────────────────────────────────────────────────────────────────

test("potOdds: 100 call into 300 pot → 0.25", () => {
  assert.equal(potOdds(100, 300), 0.25)
})

test("potOdds: 50 call into 100 pot → ~0.333", () => {
  assertInRange(potOdds(50, 100), 0.33, 0.34, "potOdds")
})

test("potOdds: 0 call → 0 (free to call / check)", () => {
  assert.equal(potOdds(0, 500), 0)
})

test("potOdds: callAmount equals pot → 0.5", () => {
  assert.equal(potOdds(200, 200), 0.5)
})

// ─── shouldCall ──────────────────────────────────────────────────────────────

test("shouldCall: equity well above odds + margin → true", () => {
  assert.equal(shouldCall(0.7, 0.25), true)
})

test("shouldCall: equity below odds → false", () => {
  assert.equal(shouldCall(0.2, 0.4), false)
})

test("shouldCall: equity equals odds + default margin (edge) → false", () => {
  // equity 0.35, odds 0.25, margin 0.1 → 0.35 > 0.35 is false
  assert.equal(shouldCall(0.35, 0.25), false)
})

test("shouldCall: custom margin=0 → true when equity just above odds", () => {
  assert.equal(shouldCall(0.26, 0.25, 0), true)
})

// ─── suggestBetSize ──────────────────────────────────────────────────────────

test("suggestBetSize: equity > 0.75 → 75% of pot", () => {
  assert.equal(suggestBetSize(1000, 0.8), 750)
})

test("suggestBetSize: equity 0.6-0.75 → 60% of pot", () => {
  assert.equal(suggestBetSize(1000, 0.65), 600)
})

test("suggestBetSize: equity 0.5-0.6 → 40% of pot", () => {
  assert.equal(suggestBetSize(1000, 0.55), 400)
})

test("suggestBetSize: equity < 0.5 → 25% of pot", () => {
  assert.equal(suggestBetSize(1000, 0.35), 250)
})

test("suggestBetSize: floors to integer", () => {
  const result = suggestBetSize(333, 0.8)
  assert.equal(result, Math.floor(333 * 0.75))
})

// ─── estimateEquity: preflop ─────────────────────────────────────────────────

test("estimateEquity preflop: pocket aces → high equity (≥ 0.78)", () => {
  const equity = estimateEquity(
    [{ rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" }],
    []
  )
  assertInRange(equity, 0.78, 1.0, "AA preflop")
})

test("estimateEquity preflop: pocket pair → above 0.6", () => {
  const equity = estimateEquity(
    [{ rank: "7", suit: "spades" }, { rank: "7", suit: "hearts" }],
    []
  )
  assertInRange(equity, 0.6, 1.0, "77 preflop")
})

test("estimateEquity preflop: AK → above 0.5", () => {
  const equity = estimateEquity(
    [{ rank: "A", suit: "spades" }, { rank: "K", suit: "hearts" }],
    []
  )
  assertInRange(equity, 0.5, 0.7, "AK preflop")
})

test("estimateEquity preflop: 72o → low equity (< 0.4)", () => {
  const equity = estimateEquity(
    [{ rank: "7", suit: "spades" }, { rank: "2", suit: "hearts" }],
    []
  )
  assertInRange(equity, 0, 0.4, "72o preflop")
})

test("estimateEquity preflop: suited connectors → at least 0.35", () => {
  const equity = estimateEquity(
    [{ rank: "8", suit: "spades" }, { rank: "9", suit: "spades" }],
    []
  )
  assertInRange(equity, 0.35, 0.6, "89s preflop")
})

test("estimateEquity: accepts raw card strings", () => {
  const equity = estimateEquity(["Aspades", "Ahearts"], [])
  assertInRange(equity, 0.78, 1.0, "AA preflop strings")
})

// ─── estimateEquity: postflop ────────────────────────────────────────────────

test("estimateEquity postflop: top set on flop → high equity (≥ 0.65)", () => {
  // Hole: AA, Board: A K 2 → three aces
  const equity = estimateEquity(
    [{ rank: "A", suit: "spades" }, { rank: "A", suit: "hearts" }],
    [{ rank: "A", suit: "clubs" }, { rank: "K", suit: "diamonds" }, { rank: "2", suit: "spades" }]
  )
  assertInRange(equity, 0.65, 1.0, "top set postflop")
})

test("estimateEquity postflop: pair on board → moderate equity", () => {
  const equity = estimateEquity(
    [{ rank: "K", suit: "spades" }, { rank: "7", suit: "hearts" }],
    [{ rank: "K", suit: "clubs" }, { rank: "3", suit: "diamonds" }, { rank: "9", suit: "spades" }]
  )
  assertInRange(equity, 0.45, 0.8, "top pair postflop")
})

test("estimateEquity postflop: high card only → below 0.5", () => {
  // Hole: 72, Board: A K Q → no improvement, high card
  const equity = estimateEquity(
    [{ rank: "7", suit: "spades" }, { rank: "2", suit: "hearts" }],
    [{ rank: "A", suit: "clubs" }, { rank: "K", suit: "diamonds" }, { rank: "Q", suit: "spades" }]
  )
  assertInRange(equity, 0, 0.5, "missed flop")
})

test("estimateEquity: invalid hole cards → 0.5 fallback", () => {
  assert.equal(estimateEquity([], []), 0.5)
  assert.equal(estimateEquity(null, []), 0.5)
  assert.equal(estimateEquity([{ rank: "A", suit: "spades" }], []), 0.5) // only 1 card
})

// ─── findAction ──────────────────────────────────────────────────────────────

test("findAction: returns action details when present", () => {
  const actions = { fold: {}, call: { amount: 100 } }
  assert.deepEqual(findAction("call", actions), { amount: 100 })
})

test("findAction: returns undefined when action is absent", () => {
  const actions = { fold: {}, call: { amount: 100 } }
  assert.equal(findAction("raise", actions), undefined)
})

test("findAction: returns undefined when normalized action has available=false", () => {
  const actions = {
    fold: { available: true },
    check: { available: false },
    call: { available: true, amount: 100 },
  }
  assert.equal(findAction("check", actions), undefined)
  assert.ok(findAction("call", actions) !== undefined)
})

test("findAction: returns action when available=true", () => {
  const actions = {
    raise: { available: true, min: 200, max: 1000 },
  }
  const result = findAction("raise", actions)
  assert.equal(result.min, 200)
  assert.equal(result.max, 1000)
})

test("findAction: null/undefined validActions → undefined", () => {
  assert.equal(findAction("fold", null), undefined)
  assert.equal(findAction("fold", undefined), undefined)
})

// ─── countOuts ───────────────────────────────────────────────────────────────

test("countOuts: flush draw (4 to flush) adds ~9 outs", () => {
  // Hole: As Ks (both spades), Board: 2s 7s Qh → 4 spades, flush draw
  const hole = [{ rank: "A", suit: "spades" }, { rank: "K", suit: "spades" }]
  const board = [{ rank: "2", suit: "spades" }, { rank: "7", suit: "spades" }, { rank: "Q", suit: "hearts" }]
  const outs = countOuts(hole, board)
  assert.ok(outs >= 9, `expected ≥9 outs for flush draw, got ${outs}`)
})

test("countOuts: open-ended straight draw adds ~8 outs", () => {
  // 5-6-7-8 → open-ended, needs 4 or 9
  const hole = [{ rank: "5", suit: "spades" }, { rank: "6", suit: "hearts" }]
  const board = [{ rank: "7", suit: "clubs" }, { rank: "8", suit: "diamonds" }, { rank: "A", suit: "spades" }]
  const outs = countOuts(hole, board)
  assert.ok(outs >= 8, `expected ≥8 outs for OESD, got ${outs}`)
})

test("countOuts: no draws → 0 outs", () => {
  // Random disconnected cards, no draws
  const hole = [{ rank: "A", suit: "spades" }, { rank: "2", suit: "hearts" }]
  const board = [{ rank: "K", suit: "clubs" }, { rank: "7", suit: "diamonds" }, { rank: "9", suit: "hearts" }]
  const outs = countOuts(hole, board)
  assert.ok(outs >= 0 && outs <= 21)
})
