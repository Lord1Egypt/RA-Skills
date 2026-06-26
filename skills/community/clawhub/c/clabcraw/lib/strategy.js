/**
 * Poker strategy helpers for Clabcraw agent decision-making.
 *
 * Provides hand evaluation, pot odds, and bet sizing utilities.
 * Works with both raw card strings ("Aspades") and normalized card objects
 * ({ rank, suit }) from lib/schema.js.
 */

const RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

/**
 * Parse a card string like "Aspades" into { rank, suit }.
 * Already-parsed objects are returned as-is.
 *
 * @param {string|{rank:string,suit:string}} card
 * @returns {{ rank: string, suit: string }}
 */
function parseCard(card) {
  if (typeof card === "object" && card !== null && card.rank) return card
  if (typeof card !== "string" || card.length < 2) return { rank: "?", suit: "?" }
  const rank = card.startsWith("10") ? "10" : card[0]
  const suit = card.slice(rank.length)
  return { rank, suit }
}

function rankIndex(rank) {
  return RANKS.indexOf(rank)
}

// ─── Hand ranking ──────────────────────────────────────────────────────────────

/**
 * Evaluate the best 5-card hand rank from up to 7 cards.
 * Returns a numeric rank 0 (high card) through 8 (straight flush).
 *
 * @param {Array<{rank:string,suit:string}>} cards - 2-7 card objects
 * @returns {number} 0=high card, 1=pair, 2=two pair, 3=trips, 4=straight,
 *                   5=flush, 6=full house, 7=quads, 8=straight flush
 */
export function handRank(cards) {
  if (!cards || cards.length < 2) return 0

  const parsed = cards.map(parseCard)
  const ranks = parsed.map((c) => rankIndex(c.rank))
  const suits = parsed.map((c) => c.suit)

  const rankCounts = {}
  for (const r of ranks) rankCounts[r] = (rankCounts[r] || 0) + 1

  const counts = Object.values(rankCounts).sort((a, b) => b - a)
  const uniqueRanks = [...new Set(ranks)].sort((a, b) => a - b)

  const suitCounts = {}
  for (const s of suits) suitCounts[s] = (suitCounts[s] || 0) + 1
  const hasFlush = Object.values(suitCounts).some((c) => c >= 5)

  const hasStraight = _hasStraight(uniqueRanks)

  if (hasFlush && hasStraight) return 8
  if (counts[0] === 4) return 7
  if (counts[0] === 3 && counts[1] === 2) return 6
  if (hasFlush) return 5
  if (hasStraight) return 4
  if (counts[0] === 3) return 3
  if (counts[0] === 2 && counts[1] === 2) return 2
  if (counts[0] === 2) return 1
  return 0
}

/**
 * Human-readable hand description.
 *
 * @param {Array<{rank:string,suit:string}>} cards
 * @returns {string}
 */
export function describeHand(cards) {
  const NAMES = [
    "High card", "Pair", "Two pair", "Three of a kind",
    "Straight", "Flush", "Full house", "Four of a kind", "Straight flush",
  ]
  return NAMES[handRank(cards)] || "Unknown"
}

/**
 * Count approximate outs to improve the hand on the next street.
 *
 * @param {Array<{rank:string,suit:string}>} hole - 2 hole cards
 * @param {Array<{rank:string,suit:string}>} board - 3-4 community cards
 * @returns {number} Approximate number of outs
 */
export function countOuts(hole, board) {
  const allCards = [...hole, ...board].map(parseCard)
  const current = handRank(allCards)
  let outs = 0

  // Flush draw: 4 cards of same suit
  const suits = allCards.map((c) => c.suit)
  const suitCounts = {}
  for (const s of suits) suitCounts[s] = (suitCounts[s] || 0) + 1
  if (Object.values(suitCounts).some((c) => c === 4)) outs += 9

  // Open-ended straight draw
  const ranks = [...new Set(allCards.map((c) => rankIndex(c.rank)))].sort((a, b) => a - b)
  if (_hasOpenEndedDraw(ranks)) outs += 8

  // Gutshot straight draw
  if (_hasGutshotDraw(ranks)) outs += 4

  // Improve pair to trips (or trips to quads)
  if (current === 1) outs += 2  // pair → trips
  if (current === 2) outs += 4  // two pair → full house

  return Math.min(outs, 21) // cap at 21 (outs overlap)
}

// ─── Equity estimation ────────────────────────────────────────────────────────

/**
 * Estimate hand equity at any street.
 *
 * Preflop (no community cards): uses heuristic based on hole card strength.
 * Flop/Turn/River: evaluates made hand rank + draw outs.
 *
 * Accepts either raw card strings or normalized { rank, suit } objects.
 *
 * @param {Array<string|{rank:string,suit:string}>} holeCards - 2 hole cards
 * @param {Array<string|{rank:string,suit:string}>} [communityCards=[]] - 0-5 board cards
 * @returns {number} Estimated equity 0.0–1.0
 */
export function estimateEquity(holeCards, communityCards = []) {
  if (!holeCards || holeCards.length !== 2) return 0.5

  const hole = holeCards.map(parseCard)
  const board = (communityCards || []).map(parseCard)

  if (board.length === 0) {
    return _preflopEquity(hole)
  }

  return _postflopEquity(hole, board)
}

// ─── Pot odds & bet sizing ────────────────────────────────────────────────────

/**
 * Calculate pot odds.
 *
 * @param {number} callAmount - Amount needed to call
 * @param {number} currentPot - Current pot size
 * @returns {number} Pot odds ratio (0.0–1.0)
 */
export function potOdds(callAmount, currentPot) {
  if (callAmount <= 0) return 0
  return callAmount / (currentPot + callAmount)
}

/**
 * Check if calling is profitable given equity and pot odds.
 *
 * @param {number} equity - Estimated hand equity (0.0–1.0)
 * @param {number} odds - Pot odds ratio from potOdds()
 * @param {number} [margin=0.1] - Safety margin
 * @returns {boolean}
 */
export function shouldCall(equity, odds, margin = 0.1) {
  return equity > odds + margin
}

/**
 * Suggest bet size as a fraction of pot.
 *
 * @param {number} pot - Current pot size
 * @param {number} equity - Estimated hand equity
 * @returns {number} Suggested bet amount
 */
export function suggestBetSize(pot, equity) {
  if (equity > 0.75) return Math.floor(pot * 0.75)
  if (equity > 0.6) return Math.floor(pot * 0.6)
  if (equity > 0.5) return Math.floor(pot * 0.4)
  return Math.floor(pot * 0.25)
}

/**
 * Check if a valid action exists and return its details.
 *
 * Works with both raw valid_actions objects and normalized state.actions maps.
 *
 * @param {string} actionName - "fold", "check", "call", "raise", "all_in"
 * @param {object} validActions - Object keyed by action name
 * @returns {object|undefined}
 */
export function findAction(actionName, validActions) {
  if (!validActions || !(actionName in validActions)) return undefined
  const action = validActions[actionName]
  // Support normalized actions ({ available: false }) — return undefined if not available
  if (action && action.available === false) return undefined
  return action
}

// ─── Internal helpers ─────────────────────────────────────────────────────────

function _preflopEquity(hole) {
  const c1 = hole[0]
  const c2 = hole[1]
  const r1 = rankIndex(c1.rank)
  const r2 = rankIndex(c2.rank)

  if (c1.rank === c2.rank) {
    return 0.6 + (r1 / 13) * 0.2  // pocket pair: 60–80%
  }

  const isAce = r1 === 12 || r2 === 12
  const isBroadway = r1 >= 9 && r2 >= 9

  if (isAce && isBroadway) return 0.55  // AK, AQ, AJ
  if (isBroadway) return 0.5            // KQ, KJ, QJ, etc.
  if (r1 >= 9 || r2 >= 9) return 0.4   // one broadway

  const suited = c1.suit === c2.suit
  const connected = Math.abs(r1 - r2) === 1
  if (suited && connected) return 0.4   // suited connectors

  return 0.35
}

function _postflopEquity(hole, board) {
  const allCards = [...hole, ...board]
  const rank = handRank(allCards)

  // Base equity from made hand strength
  // handRank 0-8 → base equity 0.35-0.92
  const BASE = [0.35, 0.50, 0.60, 0.68, 0.74, 0.78, 0.84, 0.91, 0.95]
  let equity = BASE[rank] ?? 0.35

  // Add equity from draws (outs → implied equity using rule of 2/4)
  const cardsToGo = 5 - board.length
  if (cardsToGo > 0 && rank < 5) {
    const outs = countOuts(hole, board)
    const drawEquity = outs * (cardsToGo === 1 ? 0.02 : 0.04)
    equity = Math.min(0.95, equity + drawEquity * (1 - equity))
  }

  return equity
}

function _hasStraight(sortedUniqueRanks) {
  // Ace-low straight: A-2-3-4-5 → ranks include 0,1,2,3,12
  const withLowAce = sortedUniqueRanks.includes(12)
    ? [...sortedUniqueRanks, -1].sort((a, b) => a - b)
    : sortedUniqueRanks

  for (let i = 0; i <= withLowAce.length - 5; i++) {
    const slice = withLowAce.slice(i, i + 5)
    if (slice[4] - slice[0] === 4 && new Set(slice).size === 5) return true
  }
  return false
}

function _hasOpenEndedDraw(sortedRanks) {
  for (let i = 0; i <= sortedRanks.length - 4; i++) {
    const slice = sortedRanks.slice(i, i + 4)
    if (slice[3] - slice[0] === 3 && new Set(slice).size === 4) return true
  }
  return false
}

function _hasGutshotDraw(sortedRanks) {
  for (let i = 0; i <= sortedRanks.length - 4; i++) {
    const slice = sortedRanks.slice(i, i + 4)
    if (slice[3] - slice[0] === 4 && new Set(slice).size === 4) return true
  }
  return false
}
