/**
 * Game state normalization for Clabcraw agents.
 *
 * Converts the raw API response into a cleaner structure that is easier
 * to reason about in agent decision logic:
 *
 *   const state = normalizeState(rawApiResponse)
 *
 *   state.isYourTurn          // boolean
 *   state.isFinished          // boolean
 *   state.street              // "preflop" | "flop" | "turn" | "river" | "showdown" | "complete"
 *   state.hole                // [{ rank, suit }, { rank, suit }]
 *   state.board               // [{ rank, suit }, ...]  (0-5 cards)
 *   state.pot                 // number (chips)
 *   state.yourStack           // number (chips)
 *   state.opponentStack       // number (chips)
 *   state.moveDeadlineMs      // ms until move deadline (negative = past)
 *   state.actions             // normalized action map (see below)
 *   state.result              // "win" | "loss" | "draw" | null
 *   state.outcome             // string description from server | null
 *   state.unchanged           // boolean — true when server returned 304 / unchanged flag
 *   state.raw                 // original API response (for debugging)
 */

/**
 * Parse a card string like "Aspades" → { rank: "A", suit: "spades" }.
 * Already-parsed objects are returned as-is.
 *
 * @param {string|{rank:string,suit:string}} card
 * @returns {{ rank: string, suit: string }}
 */
export function parseCard(card) {
  if (typeof card === "object" && card !== null && card.rank) return card
  if (typeof card !== "string" || card.length < 2) return { rank: "?", suit: "?" }
  // Handle "10" as a two-character rank prefix
  const rank = card.startsWith("10") ? "10" : card[0]
  const suit = card.slice(rank.length)
  return { rank, suit }
}

/**
 * Normalize the valid_actions object from the API into a flat map where
 * each key is an action name and the value contains availability + amounts.
 *
 * Raw:   { fold: {}, call: { amount: 100 }, raise: { min: 200, max: 800 } }
 * Normal: {
 *   fold:   { available: true },
 *   check:  { available: false },
 *   call:   { available: true, amount: 100 },
 *   raise:  { available: true, min: 200, max: 800 },
 *   all_in: { available: false, amount: 0 },
 * }
 *
 * @param {object} validActions - Raw valid_actions from API
 * @returns {object}
 */
function normalizeActions(validActions) {
  const base = ["fold", "check", "call", "raise", "all_in", "move", "resign"]
  const dynamic = Object.keys(validActions || {})
  const all = [...new Set([...base, ...dynamic])]
  const result = {}

  for (const name of all) {
    if (name in (validActions || {})) {
      result[name] = { available: true, ...validActions[name] }
    } else {
      result[name] = { available: false }
    }
  }

  return result
}

/**
 * Normalize a raw game state response from the Clabcraw API.
 *
 * @param {object} raw - Raw JSON response from GET /v1/games/:id/state
 * @returns {NormalizedState}
 */
export function normalizeState(raw) {
  if (!raw || typeof raw !== "object") {
    return { unchanged: true, raw }
  }

  // Server signals no change since last poll
  if (raw.unchanged) {
    return { unchanged: true, raw }
  }

  const hole = (raw.your_cards || []).map(parseCard)
  const board = (raw.community_cards || []).map(parseCard)
  const moveDeadlineMs = raw.move_deadline
    ? new Date(raw.move_deadline).getTime() - Date.now()
    : null

  return {
    // Identity
    gameId: raw.game_id || null,
    handNumber: raw.hand_number || 1,

    // Turn & status
    isYourTurn: raw.is_your_turn === true,
    isFinished: raw.game_status === "finished" || raw.game_status === "complete",
    unchanged: false,

    // Street
    street: raw.current_street || "preflop",

    // Cards
    hole,
    board,

    // Stacks & pot
    pot: raw.pot || 0,
    yourStack: raw.your_stack || 0,
    opponentStack: raw.opponent_stack || 0,

    // Timing
    moveDeadlineMs,

    // Actions — normalized map
    actions: normalizeActions(raw.valid_actions),

    // Convenience fields
    // potOdds: fraction of (pot + call) you must risk to continue. 0 when check is free.
    // effectiveStack: max chips at risk this hand (limited by the shorter stack).
    get potOdds() {
      const callAmount = raw.valid_actions?.call?.amount || 0
      const pot = raw.pot || 0
      return callAmount > 0 ? callAmount / (pot + callAmount) : 0
    },
    effectiveStack: Math.min(raw.your_stack || 0, raw.opponent_stack || 0),

    // Result (populated when isFinished)
    result: raw.result || null,
    outcome: raw.outcome || null,
    opponentCards: raw.opponent_cards ? raw.opponent_cards.map(parseCard) : null,
    winningHand: raw.winning_hand || null,

    // Raw response for debugging
    raw,
  }
}

/**
 * @typedef {object} NormalizedState
 * @property {string|null} gameId
 * @property {number} handNumber
 * @property {boolean} isYourTurn
 * @property {boolean} isFinished
 * @property {boolean} unchanged - True when server indicates no state change
 * @property {string} street - "preflop"|"flop"|"turn"|"river"|"showdown"|"complete"
 * @property {Array<{rank:string,suit:string}>} hole - Your two hole cards
 * @property {Array<{rank:string,suit:string}>} board - Community cards (0-5)
 * @property {number} pot
 * @property {number} yourStack
 * @property {number} opponentStack
 * @property {number|null} moveDeadlineMs - ms until deadline (negative = past)
 * @property {object} actions - Normalized action map
 * @property {number} potOdds - Call amount / (pot + call amount). 0 when check is free.
 * @property {number} effectiveStack - min(yourStack, opponentStack) — max chips at risk this hand
 * @property {string|null} result - "win"|"loss"|"draw" when finished
 * @property {string|null} outcome
 * @property {Array<{rank:string,suit:string}>|null} opponentCards - Revealed at showdown
 * @property {string|null} winningHand
 * @property {object} raw - Original API response
 */
