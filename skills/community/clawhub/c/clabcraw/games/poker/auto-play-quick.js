#!/usr/bin/env node

/**
 * Quick-play agent: plays normally for the first five hands, then goes all-in
 * every action from hand 6 onwards. Games end fast, useful for local testing.
 *
 * Usage:
 *   node games/poker/auto-play-quick.js
 *
 * Local play (two terminals, different wallets):
 *   CLABCRAW_API_URL=http://localhost:4000 \
 *   CLABCRAW_WALLET_PRIVATE_KEY=0x... \
 *   node games/poker/auto-play-quick.js | jq .
 */

import { GameClient } from "../../lib/game.js"
import { estimateEquity, potOdds, shouldCall, suggestBetSize, findAction } from "../../lib/strategy.js"
import { logger } from "../../lib/logger.js"
import { PausedError, InsufficientFundsError, GameDisabledError } from "../../lib/errors.js"

const GAME_TYPE = process.env.CLABCRAW_GAME_TYPE || "poker"
const MATCH_TIMEOUT_MS = parseInt(process.env.CLABCRAW_MATCH_TIMEOUT_MS || "") || 4 * 60 * 1000
const NORMAL_PLAY_HANDS = 5  // play normally for this many hands, then shove

/**
 * Normal heuristic strategy — used for hands 1 and 2.
 *
 * @param {import('../../lib/schema.js').NormalizedState} state
 * @returns {{ action: string, amount?: number }}
 */
function decideNormal(state) {
  const { hole, board, pot, actions } = state
  const callAmount = actions.call?.amount || 0
  const equity = estimateEquity(hole, board)
  const odds = potOdds(callAmount, pot || 1)

  if (equity > 0.6 && findAction("raise", actions)) {
    const raise = findAction("raise", actions)
    const suggested = suggestBetSize(pot || 100, equity)
    const clamped = Math.max(raise.min || suggested, Math.min(suggested, raise.max || suggested))
    return { action: "raise", amount: clamped }
  }

  if (shouldCall(equity, odds) && findAction("call", actions)) return { action: "call" }
  if (findAction("check", actions)) return { action: "check" }
  if (findAction("call", actions)) return { action: "call" }
  return { action: "fold" }
}

/**
 * All-in strategy — used from hand 3 onwards to end games quickly.
 * Prefers the explicit all_in action; falls back to raise-to-max.
 *
 * @param {import('../../lib/schema.js').NormalizedState} state
 * @returns {{ action: string, amount?: number }}
 */
function decideAllIn(state) {
  const { actions } = state

  if (findAction("all_in", actions)) return { action: "all_in" }

  if (findAction("raise", actions)) {
    const raise = findAction("raise", actions)
    return { action: "raise", amount: raise.max }
  }

  if (findAction("call", actions)) return { action: "call" }
  return { action: "fold" }
}

/**
 * @param {import('../../lib/schema.js').NormalizedState} state
 * @returns {{ action: string, amount?: number }}
 */
function decideAction(state) {
  const isQuickMode = state.handNumber > NORMAL_PLAY_HANDS

  logger.debug("decision", {
    hand_number: state.handNumber,
    mode: isQuickMode ? "all_in" : "normal",
    street: state.street,
  })

  return isQuickMode ? decideAllIn(state) : decideNormal(state)
}

async function main() {
  const game = new GameClient()
  logger.info("agent_ready", { address: game.address, game_type: GAME_TYPE })

  // Fetch live platform info — confirms game is available and gets current fees
  const info = await game.getPlatformInfo()
  const gameInfo = info?.games?.[GAME_TYPE]
  if (!gameInfo) {
    logger.error("game_not_available", { game_type: GAME_TYPE, available: Object.keys(info?.games || {}) })
    process.exit(1)
  }
  logger.info("platform_info", {
    game_type: GAME_TYPE,
    fee_usdc: gameInfo.entry_fee_usdc,
    skill_version: info?.skill?.version,
  })

  // Join queue
  logger.info("joining_queue", {})
  let joinResult
  try {
    joinResult = await game.join(GAME_TYPE)
  } catch (err) {
    if (err instanceof InsufficientFundsError) {
      logger.error("join_failed", { code: err.code, error: err.message })
      logger.error("hint", { message: "Fund your wallet with USDC on Base to pay the entry fee" })
    } else if (err instanceof GameDisabledError) {
      logger.error("join_failed", { code: err.code, error: err.message, available_games: err.availableGames })
      logger.error("hint", { message: `Set CLABCRAW_GAME_TYPE to one of: ${err.availableGames.join(", ")}` })
    } else if (err instanceof PausedError) {
      logger.error("join_failed", { code: err.code, error: err.message, retry_after_ms: err.retryAfterMs })
    } else {
      logger.error("join_failed", { error: err.message })
    }
    process.exit(1)
  }

  logger.info("joined_queue", { status: joinResult.status, queue_position: joinResult.queuePosition })

  // Wait for match
  logger.info("waiting_for_match", { timeout_ms: MATCH_TIMEOUT_MS })
  let gameId
  try {
    gameId = await game.waitForMatch({ timeoutMs: MATCH_TIMEOUT_MS })
    logger.info("matched", { game_id: gameId })
  } catch (err) {
    logger.error("match_failed", { code: err.code, error: err.message })
    process.exit(1)
  }

  // Play game
  const baseUrl = (process.env.CLABCRAW_API_URL || "https://clabcraw.sh").replace(/\/api$/, "")
  logger.info("game_started", { game_id: gameId, quick_mode_from_hand: NORMAL_PLAY_HANDS + 1, watch_url: `${baseUrl}/watch/${gameId}` })
  let lastHand = -1

  try {
    const finalState = await game.playUntilDone(gameId, async (state) => {
      // Log new hands
      if (state.handNumber !== lastHand) {
        lastHand = state.handNumber
        logger.info("new_hand", {
          hand: state.handNumber,
          mode: state.handNumber > NORMAL_PLAY_HANDS ? "all_in" : "normal",
          street: state.street,
          your_stack: state.yourStack,
          opponent_stack: state.opponentStack,
        })
      }

      if (!state.isYourTurn) return null

      const action = decideAction(state)
      logger.info("action_taken", { action: action.action, amount: action.amount || null })
      return action
    })

    logger.info("game_over", {
      result: finalState.result,
      outcome: finalState.outcome,
      your_stack: finalState.yourStack,
      opponent_stack: finalState.opponentStack,
      replay_url: `${baseUrl}/replay/${gameId}`,
    })
  } catch (err) {
    logger.error("game_error", { code: err.code, error: err.message })
    process.exit(1)
  }

  // Check claimable balance
  try {
    const { claimableUsdc } = await game.getClaimable()
    if (parseFloat(claimableUsdc) > 0) {
      logger.info("claimable_balance", { amount_usdc: claimableUsdc })
    }
  } catch {
    // Non-critical
  }

  logger.info("session_complete", {})
}

main().catch((err) => {
  logger.error("fatal", { error: err.message })
  process.exit(1)
})
