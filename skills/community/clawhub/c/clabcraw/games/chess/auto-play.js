#!/usr/bin/env node

/**
 * Chess auto-play agent: joins a chess game and plays with a greedy capture strategy.
 *
 * Strategy:
 *   1. If any valid move captures an opponent piece, pick one at random.
 *   2. Otherwise, pick a random move from the full valid-moves list.
 *
 * This dramatically speeds up games vs. pure random play because pieces get
 * traded off the board quickly.
 *
 * Usage:
 *   CLABCRAW_GAME_TYPE=chess \
 *   CLABCRAW_API_URL=http://localhost:4000 \
 *   CLABCRAW_WALLET_PRIVATE_KEY=0x... \
 *   node games/chess/auto-play.js
 */

import { GameClient } from "../../lib/game.js"
import { logger } from "../../lib/logger.js"
import { PausedError, InsufficientFundsError, GameDisabledError } from "../../lib/errors.js"

const GAME_TYPE = process.env.CLABCRAW_GAME_TYPE || "chess"
const MATCH_TIMEOUT_MS = parseInt(process.env.CLABCRAW_MATCH_TIMEOUT_MS || "") || 4 * 60 * 1000
const POLL_MS = 500

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)]
}

/**
 * Decide a chess action from the normalized state.
 *
 * Prefers capturing moves (destination square has an opponent piece).
 * Falls back to a random legal move. Resigns if no moves are available.
 *
 * @param {import('../../lib/schema.js').NormalizedState} state
 * @returns {{ action: string, move?: string }}
 */
function decideChessAction(state) {
  const moveAction = state.actions.move
  if (!moveAction?.available) {
    return { action: "resign" }
  }

  const moves = moveAction.examples || []
  if (moves.length === 0) {
    return { action: "resign" }
  }

  const board = state.raw.board || {}
  const myColor = state.raw.your_color // "w" or "b"

  // A move is a capture if the destination square has an opponent's piece.
  // UCI format: "e2e4" → from=e2, to=e4. Promotions like "e7e8q" are also handled.
  const captures = moves.filter((uci) => {
    const to = uci.slice(2, 4)
    const piece = board[to]
    return piece && piece.color !== myColor
  })

  const chosen = captures.length > 0 ? pickRandom(captures) : pickRandom(moves)

  logger.debug("chess_decision", {
    total_moves: moves.length,
    captures_found: captures.length,
    chosen,
  })

  return { action: "move", move: chosen }
}

async function main() {
  const game = new GameClient()
  logger.info("agent_ready", { address: game.address, game_type: GAME_TYPE })

  const info = await game.getPlatformInfo()
  const gameInfo = info?.games?.[GAME_TYPE]
  if (!gameInfo) {
    logger.error("game_not_available", { game_type: GAME_TYPE, available: Object.keys(info?.games || {}) })
    process.exit(1)
  }
  logger.info("platform_info", { game_type: GAME_TYPE, fee_usdc: gameInfo.entry_fee_usdc })

  logger.info("joining_queue", {})
  let joinResult
  try {
    joinResult = await game.join(GAME_TYPE)
  } catch (err) {
    if (err instanceof InsufficientFundsError) {
      logger.error("join_failed", { code: err.code, error: err.message })
    } else if (err instanceof GameDisabledError) {
      logger.error("join_failed", { code: err.code, error: err.message, available_games: err.availableGames })
    } else if (err instanceof PausedError) {
      logger.error("join_failed", { code: err.code, error: err.message })
    } else {
      logger.error("join_failed", { error: err.message })
    }
    process.exit(1)
  }

  logger.info("joined_queue", { status: joinResult.status, queue_position: joinResult.queuePosition })

  logger.info("waiting_for_match", { timeout_ms: MATCH_TIMEOUT_MS })
  let gameId
  try {
    gameId = await game.waitForMatch({ timeoutMs: MATCH_TIMEOUT_MS })
    logger.info("matched", { game_id: gameId })
  } catch (err) {
    logger.error("match_failed", { code: err.code, error: err.message })
    process.exit(1)
  }

  const baseUrl = (process.env.CLABCRAW_API_URL || "https://clabcraw.sh").replace(/\/api$/, "")
  logger.info("game_started", { game_id: gameId, watch_url: `${baseUrl}/watch/${gameId}` })

  try {
    const finalState = await game.playUntilDone(
      gameId,
      async (state) => {
        if (!state.isYourTurn) return null

        const action = decideChessAction(state)
        logger.info("action_taken", { action: action.action, move: action.move || null })
        return action
      },
      { pollMs: POLL_MS }
    )

    logger.info("game_over", {
      result: finalState.result,
      outcome: finalState.outcome,
      replay_url: `${baseUrl}/replay/${gameId}`,
    })
  } catch (err) {
    logger.error("game_error", { code: err.code, error: err.message })
    process.exit(1)
  }

  logger.info("session_complete", {})
}

main().catch((err) => {
  logger.error("fatal", { error: err.message })
  process.exit(1)
})
