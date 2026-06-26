#!/usr/bin/env node

/**
 * Auto-play agent: Joins a game and plays with a simple equity-based strategy.
 *
 * Uses the GameClient API from lib/game.js — no shell-out to bins.
 * Strategy errors are handled via typed errors from lib/errors.js.
 *
 * Usage:
 *   node games/poker/auto-play.js
 *
 * Local play (two terminals, different wallets):
 *   CLABCRAW_API_URL=http://localhost:4000 \
 *   CLABCRAW_WALLET_PRIVATE_KEY=0x... \
 *   node games/poker/auto-play.js | jq .
 */

import { GameClient } from "../../lib/game.js"
import { estimateEquity, potOdds, shouldCall, suggestBetSize, findAction } from "../../lib/strategy.js"
import { logger } from "../../lib/logger.js"
import { PausedError, InsufficientFundsError, GameDisabledError } from "../../lib/errors.js"

const GAME_TYPE = process.env.CLABCRAW_GAME_TYPE || "poker"
const MATCH_TIMEOUT_MS = 4 * 60 * 1000  // 4 minutes
const POLL_MS = 1_000

const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

/**
 * Decide an action given a normalized game state.
 *
 * Validates all decisions against valid_actions and current stack size to prevent
 * INVALID_ACTION errors. Returns a safe fallback (check/fold) if the primary
 * strategy would violate game rules.
 *
 * @param {import('../../lib/schema.js').NormalizedState} state
 * @returns {{ action: string, amount?: number }}
 */
function decideAction(state) {
  const { hole, board, pot, actions, yourStack } = state
  const callAmount = actions.call?.amount || 0
  const equity = estimateEquity(hole, board)
  const odds = potOdds(callAmount, pot || 1)

  logger.debug("decision", {
    street: state.street,
    equity: equity.toFixed(2),
    pot_odds: odds.toFixed(2),
    call_amount: callAmount,
    your_stack: yourStack,
    hand_number: state.handNumber,
  })

  // Strong hand — raise (if available and amount is safe)
  if (equity > 0.6 && actions.raise?.available) {
    const raise = actions.raise
    const suggested = suggestBetSize(pot || 100, equity)

    // CRITICAL: Clamp to [min, max] and ensure never exceeds stack
    let amount = Math.max(
      raise.min || suggested,
      Math.min(suggested, raise.max || suggested)
    )
    // Extra safety: never exceed your current stack
    amount = Math.min(amount, yourStack)

    if (amount >= (raise.min || 0) && amount <= (raise.max || yourStack)) {
      logger.debug("raise_clamped", {
        suggested,
        clamped: amount,
        min: raise.min,
        max: raise.max,
        your_stack: yourStack,
      })
      return { action: "raise", amount }
    }
    // If clamping failed somehow, fall through to next option
    logger.debug("raise_unsafe", { suggested, min: raise.min, max: raise.max })
  }

  // Positive EV — call (use all_in if the call would consume the entire stack,
  // since the server treats them identically and all_in is semantically cleaner)
  if (shouldCall(equity, odds) && actions.call?.available) {
    if (actions.call.amount >= yourStack) {
      return { action: "all_in" }
    }
    return { action: "call" }
  }

  // Free card
  if (actions.check?.available) {
    return { action: "check" }
  }

  // Marginal but cheap — same all_in detection
  if (actions.call?.available) {
    if (actions.call.amount >= yourStack) {
      return { action: "all_in" }
    }
    return { action: "call" }
  }

  // Last resort: fold is always available
  if (actions.fold?.available) {
    return { action: "fold" }
  }

  // Should never reach here, but fail safe
  logger.warn("no_valid_actions", { available: Object.keys(actions).filter(k => actions[k].available) })
  return { action: "fold" }
}

/**
 * Play a game to completion, recovering from invalid action errors instead of exiting.
 *
 * On INVALID_ACTION, logs a warning and immediately retries the turn with a safe
 * check/fold fallback so the agent stays in the game rather than crashing out.
 *
 * @param {GameClient} game
 * @param {string} gameId
 * @param {string} baseUrl
 * @returns {Promise<import('../../lib/schema.js').NormalizedState>}
 */
async function playGame(game, gameId, baseUrl) {
  let lastHand = -1

  while (true) {
    let state
    try {
      state = await game.getState(gameId)
    } catch (err) {
      if (err.code === "GAME_NOT_FOUND") {
        // Game completed before we polled the final state — fetch result directly
        const result = await game.getResult(gameId).catch(() => null)
        const youWon = result?.winner?.toLowerCase() === game.address.toLowerCase()
        const isDraw = result?.outcome === "draw"
        return {
          isFinished: true,
          result: isDraw ? "draw" : result ? (youWon ? "win" : "loss") : "unknown",
          outcome: result?.outcome || "unknown",
          yourStack: youWon ? result?.winner_stack : result?.loser_stack,
          opponentStack: youWon ? result?.loser_stack : result?.winner_stack,
        }
      }
      throw err
    }

    if (state.unchanged) {
      await sleep(POLL_MS)
      continue
    }

    if (state.isFinished) {
      logger.info("game_over", {
        result: state.result,
        outcome: state.outcome,
        your_stack: state.yourStack,
        opponent_stack: state.opponentStack,
        replay_url: `${baseUrl}/replay/${gameId}`,
      })
      return state
    }

    if (state.handNumber !== lastHand) {
      lastHand = state.handNumber
      logger.info("new_hand", {
        hand: state.handNumber,
        street: state.street,
        your_stack: state.yourStack,
        opponent_stack: state.opponentStack,
      })
    }

    if (!state.isYourTurn) {
      await sleep(POLL_MS)
      continue
    }

    // Decide action, falling back to check/fold if strategy throws
    let action
    try {
      action = decideAction(state)
    } catch (strategyErr) {
      logger.error("strategy_error", { error: strategyErr.message })
      action = state.actions.check?.available ? { action: "check" } : { action: "fold" }
      logger.info("action_taken_fallback", { action: action.action, reason: "strategy_error" })
    }

    // Submit action — recover from transient errors to keep the agent in the game
    try {
      logger.info("action_taken", { action: action.action, amount: action.amount || null })
      await game.submitAction(gameId, action)
    } catch (err) {
      if (err.code === "INVALID_ACTION") {
        // Action was rejected as illegal — retry this turn with a safe fallback
        logger.warn("invalid_action_fallback", {
          attempted: action,
          error: err.message,
          valid_actions: err.context?.valid_actions,
        })
        const fallback = state.actions.check?.available ? { action: "check" } : { action: "fold" }
        logger.info("action_taken_fallback", { action: fallback.action, reason: "invalid_action" })
        await game.submitAction(gameId, fallback)
      } else if (err.code === "AUTH_ERROR" && err.message === "Replay detected") {
        // The network layer retried a request the server already processed.
        // The action was accepted on the first attempt — just poll for the next state.
        logger.warn("replay_detected_continuing", {
          attempted: action,
          note: "action was already processed; skipping retry",
        })
      } else {
        throw err
      }
    }

    await sleep(POLL_MS)
  }
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
  logger.info("game_started", { game_id: gameId, watch_url: `${baseUrl}/watch/${gameId}` })

  try {
    await playGame(game, gameId, baseUrl)
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
