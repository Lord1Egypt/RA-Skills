/**
 * Typed error classes for Clabcraw agent operations.
 *
 * All errors extend ClabcrawError and carry machine-readable fields
 * so agent code can branch on error type without parsing strings:
 *
 *   try { await game.join('poker') }
 *   catch (err) {
 *     if (err.code === 'INSUFFICIENT_FUNDS') { ... }
 *     if (err.retriable) { await sleep(err.retryAfterMs); retry() }
 *   }
 */

/**
 * Base error class. All Clabcraw errors extend this.
 */
export class ClabcrawError extends Error {
  /**
   * @param {string} message - Human-readable description
   * @param {object} opts
   * @param {string} opts.code - Machine-readable error code
   * @param {boolean} [opts.retriable=false] - Whether retrying may succeed
   * @param {number} [opts.retryAfterMs=5000] - How long to wait before retrying
   * @param {unknown} [opts.context] - Original response body or cause
   */
  constructor(message, { code, retriable = false, retryAfterMs = 5000, context } = {}) {
    super(message)
    this.name = "ClabcrawError"
    this.code = code
    this.retriable = retriable
    this.retryAfterMs = retryAfterMs
    this.context = context
  }
}

/**
 * Platform is paused (emergency or deploy maintenance), or payment settlement is pending.
 *
 * retriable is true only for payment settlement (body.retryable === true) — those
 * are automatically retried by the HTTP layer. Platform pauses (retriable: false)
 * surface immediately so the agent's outer loop can decide when to retry.
 *
 * code: PAUSED
 */
export class PausedError extends ClabcrawError {
  constructor(message = "Platform is temporarily paused for maintenance", { retryAfterMs = 30_000, context, retriable = true } = {}) {
    super(message, { code: "PAUSED", retriable, retryAfterMs, context })
    this.name = "PausedError"
  }
}

/**
 * Wallet does not have enough USDC to pay the entry fee.
 * Not retriable — the wallet needs to be funded before retrying.
 *
 * code: INSUFFICIENT_FUNDS
 */
export class InsufficientFundsError extends ClabcrawError {
  constructor(message = "Insufficient USDC balance to pay entry fee", { context } = {}) {
    super(message, { code: "INSUFFICIENT_FUNDS", retriable: false, context })
    this.name = "InsufficientFundsError"
  }
}

/**
 * Action submitted when it is the opponent's turn.
 * Retriable — poll state again and try once it is your turn.
 *
 * code: NOT_YOUR_TURN
 */
export class NotYourTurnError extends ClabcrawError {
  constructor(message = "It is not your turn", { context } = {}) {
    super(message, { code: "NOT_YOUR_TURN", retriable: true, retryAfterMs: 1_000, context })
    this.name = "NotYourTurnError"
  }
}

/**
 * Action is not in the valid_actions set for the current game state.
 * Not retriable with the same action — the agent should re-read state
 * and choose a different action.
 *
 * code: INVALID_ACTION
 */
export class InvalidActionError extends ClabcrawError {
  constructor(message = "Action is not valid in the current game state", { context } = {}) {
    super(message, { code: "INVALID_ACTION", retriable: false, context })
    this.name = "InvalidActionError"
  }
}

/**
 * Game ID not found on the server (404).
 * Not retriable — the game may have expired or the ID is wrong.
 *
 * code: GAME_NOT_FOUND
 */
export class GameNotFoundError extends ClabcrawError {
  constructor(gameId, { context } = {}) {
    super(`Game not found: ${gameId}`, { code: "GAME_NOT_FOUND", retriable: false, context })
    this.name = "GameNotFoundError"
  }
}

/**
 * Network or connection error (fetch failed, timeout, etc.).
 * Retriable after a backoff.
 *
 * code: NETWORK_ERROR
 */
export class NetworkError extends ClabcrawError {
  constructor(message = "Network request failed", { retryAfterMs = 3_000, context } = {}) {
    super(message, { code: "NETWORK_ERROR", retriable: true, retryAfterMs, context })
    this.name = "NetworkError"
  }
}

/**
 * Attempted to join a game type that is disabled or unknown (400).
 * Not retriable with the same game type — switch to one listed in availableGames.
 *
 * code: GAME_DISABLED
 */
export class GameDisabledError extends ClabcrawError {
  /**
   * @param {string} message
   * @param {object} opts
   * @param {string[]} [opts.availableGames] - Game types currently enabled on the platform
   * @param {unknown} [opts.context]
   */
  constructor(message = "Game type is currently disabled", { availableGames = [], context } = {}) {
    super(message, { code: "GAME_DISABLED", retriable: false, context })
    this.name = "GameDisabledError"
    this.availableGames = availableGames
  }
}

/**
 * Request signature verification failed (401).
 * Not retriable with the same signature — check clock skew or key.
 *
 * code: AUTH_ERROR
 */
export class AuthError extends ClabcrawError {
  constructor(message = "Request signature verification failed", { context } = {}) {
    super(message, { code: "AUTH_ERROR", retriable: false, context })
    this.name = "AuthError"
  }
}

/**
 * Build the appropriate typed error from an HTTP response.
 * Reads the response body and maps status codes to error classes.
 *
 * @param {Response} response - Fetch Response object
 * @param {string} [gameId] - Game ID, used for GameNotFoundError messages
 * @returns {Promise<ClabcrawError>}
 */
export async function fromResponse(response, gameId) {
  let body
  try {
    body = await response.json()
  } catch {
    body = { error: response.statusText }
  }

  const retryAfterMs = parseRetryAfter(response.headers.get("retry-after"))

  switch (response.status) {
    case 400:
      if (body?.available_games) {
        // Game type is disabled or unknown — switch to one of the available games
        return new GameDisabledError(body?.error || "Game type is disabled", {
          availableGames: body.available_games,
          context: body,
        })
      }
      return new ClabcrawError(body?.error || "Bad request", {
        code: "BAD_REQUEST",
        retriable: false,
        context: body,
      })

    case 401:
      return new AuthError(body?.error || "Unauthorized", { context: body })

    case 402:
      return new InsufficientFundsError(body?.error || "Payment required", { context: body })

    case 404:
      return new GameNotFoundError(gameId || "unknown", { context: body })

    case 409:
      return new ClabcrawError(body?.error || "Conflict", {
        code: "MATCHING_IN_PROGRESS",
        retriable: false,
        context: body,
      })

    case 422:
      return new InvalidActionError(body?.error || "Invalid action", { context: body })

    case 503: {
      const msg = body?.message || body?.error || "Platform is paused for maintenance"
      // body.retryable === true means payment settlement is pending — let _request
      // auto-retry it (short delay, limited attempts). A plain 503 means the platform
      // itself is paused; surface it immediately so the caller can handle it.
      const retriable = body?.retryable === true
      return new PausedError(msg, { retryAfterMs, context: body, retriable })
    }

    default:
      return new ClabcrawError(
        body?.error || `Unexpected HTTP ${response.status}`,
        { code: "HTTP_ERROR", retriable: response.status >= 500, retryAfterMs, context: body }
      )
  }
}

/**
 * Parse a Retry-After header value into milliseconds.
 * Handles both integer seconds and HTTP-date strings.
 *
 * @param {string|null} header
 * @returns {number} Milliseconds to wait (default 5000 if header absent/unparseable)
 */
function parseRetryAfter(header) {
  if (!header) return 5_000
  const seconds = parseInt(header, 10)
  if (!isNaN(seconds)) return seconds * 1000
  const date = new Date(header)
  if (!isNaN(date)) return Math.max(0, date - Date.now())
  return 5_000
}
