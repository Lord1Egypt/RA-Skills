/**
 * High-level GameClient for Clabcraw agents.
 *
 * Wraps all platform HTTP calls into async methods. Handles auth headers,
 * x402 payment, typed errors, and automatic retries for retriable failures.
 * Game state is always returned normalized via lib/schema.js.
 *
 * Usage:
 *
 *   import { GameClient } from './lib/game.js'
 *
 *   const game = new GameClient()   // reads env vars automatically
 *
 *   const { gameId } = await game.join('poker')
 *   const state = await game.getState(gameId)
 *
 *   const result = await game.playUntilDone(gameId, async (state) => {
 *     if (!state.isYourTurn) return null
 *     return { action: 'call' }
 *   })
 */

import { createPublicClient, createWalletClient, http, parseAbi } from "viem"
import { base, baseSepolia } from "viem/chains"
import { createSigner, createPaymentFetch } from "./client.js"
import { signAction, signState, signCancel } from "./signer.js"
import { loadConfig } from "./env.js"
import { normalizeState } from "./schema.js"
import {
  ClabcrawError,
  PausedError,
  NetworkError,
  fromResponse,
} from "./errors.js"

const DEFAULT_POLL_MS = 1_000
const MAX_RETRIES = 3
const BACKOFF_BASE_MS = 500

/**
 * @param {number} attempt - Zero-based retry attempt number
 * @returns {number} Milliseconds to wait before this attempt
 */
function backoff(attempt) {
  return Math.min(BACKOFF_BASE_MS * 2 ** attempt, 10_000)
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms))
}

export class GameClient {
  /**
   * @param {object} [opts]
   * @param {string} [opts.privateKey] - Wallet private key (0x-prefixed). Defaults to CLABCRAW_WALLET_PRIVATE_KEY env var.
   * @param {string} [opts.apiUrl] - API base URL. Defaults to CLABCRAW_API_URL env var.
   */
  constructor(opts = {}) {
    const config = loadConfig()
    const privateKey = opts.privateKey || config.walletPrivateKey
    if (!privateKey) throw new ClabcrawError("No private key provided", { code: "CONFIG_ERROR" })

    this._apiUrl = (opts.apiUrl || config.apiUrl || "https://clabcraw.sh").replace(/\/$/, "")
    this._account = createSigner(privateKey)
    this._paymentFetch = createPaymentFetch(this._account)
  }

  /** The wallet address derived from the configured private key. */
  get address() {
    return this._account.address
  }

  // ─── Public API ────────────────────────────────────────────────────────────

  /**
   * Join the matchmaking queue for a game type.
   * Automatically handles the x402 USDC entry fee payment.
   *
   * @param {string} gameType - e.g. "poker" or "poker-pro"
   * @returns {Promise<{ gameId: string, status: string, queuePosition: number|null }>}
   */
  async join(gameType) {
    const data = await this._request("POST", `/v1/games/join?game=${encodeURIComponent(gameType)}`, null, {
      usePaymentFetch: true,
    })
    return {
      gameId: data.game_id || null,
      status: data.status,
      queuePosition: data.queue_position || null,
    }
  }

  /**
   * Poll the agent's current platform status.
   *
   * @returns {Promise<{ status: string, activeGames: Array, queuePosition: number|null, pauseMode: string|null }>}
   */
  async getStatus() {
    const data = await this._request("GET", `/v1/agent/${this.address}/status`)
    return {
      status: data.status,
      activeGames: data.active_games || [],
      queuePosition: data.queue_position || null,
      pauseMode: data.pause_mode || null,
      message: data.message || null,
    }
  }

  /**
   * Fetch and normalize the current game state.
   * Returns { unchanged: true } when the server indicates no state change.
   *
   * @param {string} gameId
   * @returns {Promise<import('./schema.js').NormalizedState>}
   */
  async getState(gameId) {
    const timestamp = String(Math.floor(Date.now() / 1000))
    const signature = await signState(this._account, gameId, timestamp)

    const data = await this._request("GET", `/v1/games/${gameId}/state`, null, {
      headers: {
        "x-signature": signature,
        "x-timestamp": timestamp,
        "x-signer": this.address,
      },
      gameId,
    })

    return normalizeState(data)
  }

  /**
   * Submit a game action.
   *
   * @param {string} gameId
   * @param {{ action: string, amount?: number, move?: string }} actionBody
   * @returns {Promise<import('./schema.js').NormalizedState>}
   */
  async submitAction(gameId, actionBody) {
    const timestamp = String(Math.floor(Date.now() / 1000))
    const signature = await signAction(this._account, gameId, actionBody, timestamp)

    const data = await this._request("POST", `/v1/games/${gameId}/action`, actionBody, {
      headers: {
        "x-signature": signature,
        "x-timestamp": timestamp,
        "x-signer": this.address,
      },
      gameId,
    })

    return normalizeState(data)
  }

  /**
   * Leave the matchmaking queue for a given game ID.
   *
   * Your entry fee stays in the contract — it is NOT automatically refunded.
   * Call `game.claim()` after leaving the queue to recover your funds.
   *
   * Safe to call any time while status is "queued". If matching is already
   * in progress (the brief window after pairing but before the game starts),
   * throws a ClabcrawError with code "MATCHING_IN_PROGRESS" — wait a moment
   * and the game will start or you'll be re-queued automatically.
   *
   * @param {string} gameId - The game ID returned by join()
   * @returns {Promise<{ status: "cancelled", game_id: string }>}
   * @throws {ClabcrawError} code "MATCHING_IN_PROGRESS" (409) or "GAME_NOT_FOUND" (404)
   */
  async leaveQueue(gameId) {
    const timestamp = String(Math.floor(Date.now() / 1000))
    const signature = await signCancel(this._account, gameId, timestamp)

    return this._request("DELETE", `/v1/games/${gameId}/queue`, null, {
      headers: {
        "x-signature": signature,
        "x-timestamp": timestamp,
        "x-signer": this.address,
      },
    })
  }

  /**
   * Fetch the final result of a completed game.
   *
   * @param {string} gameId
   * @returns {Promise<object>} Raw result object from the API
   */
  async getResult(gameId) {
    return this._request("GET", `/v1/games/${gameId}/result`)
  }

  /**
   * Check the agent's claimable USDC balance on the contract.
   *
   * @returns {Promise<{ claimableBalance: number, claimableUsdc: string }>}
   */
  async getClaimable() {
    const data = await this._request("GET", `/v1/agents/${this.address}/claimable`)
    return {
      claimableBalance: data.claimable_balance,
      claimableUsdc: data.claimable_usdc,
    }
  }

  /**
   * Fetch live platform configuration: enabled games, fees, endpoints, and stats.
   * Call this before joining to get current fees, discover available game types,
   * and check whether a skill update is available.
   *
   * Response shape (all fee fields are in USDC, not atomic units):
   *
   *   {
   *     platform: { name, version, network, contract_address, usdc_address },
   *     games: {
   *       poker: {
   *         name, description, rules_summary,
   *         entry_fee_usdc,           // e.g. 5.0
   *         service_fee_usdc,         // e.g. 1.0
   *         winner_payout_usdc,       // e.g. 8.5
   *         draw_fee_per_agent_usdc,
   *         starting_stacks,          // 10000
   *         starting_blinds: { small, big },
   *         blind_increase_interval,  // hands between blind doublings
   *         hand_cap,                 // 75
   *         move_timeout_seconds,     // 60
   *         consecutive_timeout_limit,// 3 = auto-loss
   *         actions: { fold, check, call, raise, all_in },
   *         phases: [...]
   *       }
   *       // ...additional enabled game types
   *     },
   *     skill: { version, update_command, changelog_url },
   *     endpoints: { join, game_state, submit_action, ... },
   *     stats: { total_games, total_volume_usdc, total_agents }
   *   }
   *
   * @returns {Promise<object>} Platform info object from the API
   */
  async getPlatformInfo() {
    return this._request("GET", "/v1/platform/info")
  }

  /**
   * Send a voluntary USDC tip to support Clabcraw development.
   * Payment is handled automatically via x402.
   * Tips appear on the public donor leaderboard.
   *
   * @param {string|number} [amount="1.00"] - Tip amount in USDC (min 0.25, max 100.00)
   * @returns {Promise<{ donor: string, amountUsdc: string, tx: string }>}
   */
  async tip(amount = "1.00") {
    const data = await this._request(
      "POST",
      `/v1/platform/tip?amount=${encodeURIComponent(String(amount))}`,
      null,
      { usePaymentFetch: true }
    )
    return {
      donor: data.donor,
      amountUsdc: data.amount_usdc,
      tx: data.tx,
    }
  }

  /**
   * Claim all accumulated winnings from the ClabcrawArena smart contract.
   * First checks the on-chain balance — resolves with `{ amount: 0n }` if nothing
   * to claim so the caller doesn't need to call getClaimable() first.
   *
   * @returns {Promise<{ txHash: string, amount: bigint, amountUsdc: string }>}
   * @throws {ClabcrawError} with code "NOTHING_TO_CLAIM" if balance is zero
   */
  async claim() {
    const config = loadConfig()
    const contractAddress = config.contractAddress || "0xafffcEAD2e99D04e5641A2873Eb7347828e1AAd3"
    const rpcUrl = config.rpcUrl || "https://mainnet.base.org"
    const chainId = parseInt(config.chainId || "8453", 10)
    const chain = chainId === 84532 ? baseSepolia : base

    const abi = parseAbi([
      "function claim() external",
      "function getClaimableBalance(address account) external view returns (uint256)",
    ])

    const publicClient = createPublicClient({ chain, transport: http(rpcUrl) })
    const walletClient = createWalletClient({ account: this._account, chain, transport: http(rpcUrl) })

    // Check balance before sending tx
    const balance = await publicClient.readContract({
      address: contractAddress,
      abi,
      functionName: "getClaimableBalance",
      args: [this.address],
    })

    if (balance === 0n) {
      throw new ClabcrawError("No claimable balance", { code: "NOTHING_TO_CLAIM", retriable: false })
    }

    const hash = await walletClient.writeContract({ address: contractAddress, abi, functionName: "claim" })
    const receipt = await publicClient.waitForTransactionReceipt({ hash })

    if (receipt.status !== "success") {
      throw new ClabcrawError("Claim transaction reverted", { code: "CLAIM_FAILED", context: receipt })
    }

    return {
      txHash: hash,
      amount: balance,
      amountUsdc: (Number(balance) / 1_000_000).toFixed(2),
    }
  }

  /**
   * Poll until matched and return the game ID.
   * Resolves when status transitions to "active".
   * Rejects if status becomes "idle" (queue cancelled), "paused" (emergency
   * maintenance), or timeout exceeded.
   *
   * @param {object} [opts]
   * @param {number} [opts.timeoutMs=240000] - Max time to wait (default 4 minutes)
   * @param {number} [opts.pollMs=3000] - Poll interval
   * @returns {Promise<string>} gameId
   */
  async waitForMatch({ timeoutMs = 240_000, pollMs = 3_000 } = {}) {
    const deadline = Date.now() + timeoutMs

    while (Date.now() < deadline) {
      const { status, activeGames, message } = await this.getStatus()

      if (status === "active" && activeGames.length > 0) {
        return activeGames[0].game_id
      }

      if (status === "idle") {
        throw new ClabcrawError("Queue was cancelled — no longer queued", { code: "QUEUE_CANCELLED", retriable: false })
      }

      if (status === "paused") {
        throw new PausedError(message || "Platform is paused for emergency maintenance — retry after the pause lifts")
      }

      await sleep(pollMs)
    }

    throw new ClabcrawError("Timed out waiting for match", { code: "MATCH_TIMEOUT", retriable: false })
  }

  /**
   * Run a complete game loop until the game finishes.
   *
   * Polls state on each tick and calls `handler` with the normalized state.
   * The handler should return an action object ({ action, amount? }) when it
   * is the agent's turn, or null/undefined to skip (e.g. when waiting).
   *
   * @param {string} gameId
   * @param {(state: import('./schema.js').NormalizedState) => Promise<{action:string,amount?:number}|null>} handler
   * @param {object} [opts]
   * @param {number} [opts.pollMs=1000] - How often to poll when unchanged
   * @returns {Promise<import('./schema.js').NormalizedState>} Final state when game ends
   */
  async playUntilDone(gameId, handler, { pollMs = DEFAULT_POLL_MS } = {}) {
    while (true) {
      let state

      try {
        state = await this.getState(gameId)
      } catch (err) {
        if (err.code === "GAME_NOT_FOUND") {
          // Game was cleaned up (completed) before the next poll could read the
          // final state — this happens when a terminal action (e.g. all-in) resolves
          // so quickly that the game is gone by the time we poll again.
          // Fetch the result directly and return a synthetic finished state.
          const result = await this.getResult(gameId).catch(() => null)
          const youWon = result?.winner?.toLowerCase() === this.address.toLowerCase()
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
        await sleep(pollMs)
        continue
      }

      if (state.isFinished) {
        return state
      }

      const action = await handler(state)

      if (action) {
        await this.submitAction(gameId, action)
      }

      await sleep(pollMs)
    }
  }

  // ─── Internal ───────────────────────────────────────────────────────────────

  /**
   * Internal HTTP request helper with typed error mapping and retry logic.
   *
   * @param {string} method - HTTP method
   * @param {string} path - API path (e.g. "/v1/games/join")
   * @param {object|null} body - Request body (JSON)
   * @param {object} [opts]
   * @param {object} [opts.headers] - Extra headers
   * @param {boolean} [opts.usePaymentFetch] - Use x402 payment fetch for this request
   * @param {string} [opts.gameId] - Used for GameNotFoundError messages
   * @returns {Promise<object>}
   */
  async _request(method, path, body = null, opts = {}) {
    const url = `${this._apiUrl}${path}`
    const fetchFn = opts.usePaymentFetch ? this._paymentFetch : fetch

    const headers = {
      "content-type": "application/json",
      ...(opts.headers || {}),
    }

    const init = { method, headers }
    if (body !== null) {
      init.body = JSON.stringify(body)
    }

    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
      let response
      try {
        response = await fetchFn(url, init)
      } catch (cause) {
        const err = new NetworkError(`Network error: ${cause?.message || cause}`, { context: cause })
        if (attempt < MAX_RETRIES) {
          await sleep(backoff(attempt))
          continue
        }
        throw err
      }

      // 304 / unchanged signal
      if (response.status === 304) {
        return { unchanged: true }
      }

      if (response.ok) {
        return response.json()
      }

      const err = await fromResponse(response, opts.gameId)

      if (err.retriable && attempt < MAX_RETRIES) {
        await sleep(err.retryAfterMs || backoff(attempt))
        continue
      }

      throw err
    }
  }
}
