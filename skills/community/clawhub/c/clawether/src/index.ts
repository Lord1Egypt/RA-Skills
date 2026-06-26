import { definePluginEntry } from 'openclaw/plugin-sdk/core'
import { createPluginRuntimeStore } from 'openclaw/plugin-sdk/runtime-store'
import { Type } from '@sinclair/typebox'

const ENDPOINT = process.env.CLAWETHER_ENDPOINT ?? 'https://clawaether.com'

// ─── Runtime store: persists agent_token within this OpenClaw session ─────────
const store = createPluginRuntimeStore<{ agentToken: string | null }>({
  agentToken: process.env.CLAWETHER_AGENT_TOKEN ?? null,
})

type SessionData = {
  session_id: string
  agent_token?: string
  game_id?: string
  board: unknown
  score: number
  status: string
  legal_moves: unknown
  move_count: number
  max_tile: number
  gained?: number
}

type LeaderboardRow = {
  agent_id: string
  model: string
  score: number
  max_tile: number
  game_id?: string
}

type LeaderboardResponse = {
  leaderboard: LeaderboardRow[]
}

type ApiErrorPayload = {
  error?: string
  message?: string
  retryable?: boolean
  retry_after_ms?: number | null
  session?: SessionData
  attempted_action?: string
}

class ClawAetherApiError extends Error {
  status: number
  payload: ApiErrorPayload

  constructor(method: string, path: string, status: number, payload: ApiErrorPayload) {
    super(payload.message ?? payload.error ?? `${method} ${path} failed`)
    this.name = 'ClawAetherApiError'
    this.status = status
    this.payload = payload
  }
}

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message
  return String(error ?? 'Unknown error')
}

function extractApiError(payload: unknown): string | null {
  if (!payload || typeof payload !== 'object') return null
  const error = (payload as Record<string, unknown>).error
  return typeof error === 'string' && error.trim() ? error : null
}

async function readJsonResponse<T>(res: Response, method: string, path: string): Promise<T> {
  const raw = await res.text()
  if (!raw.trim()) {
    throw new Error(`Empty response from ${method} ${path} (HTTP ${res.status} ${res.statusText})`)
  }

  let payload: unknown
  try {
    payload = JSON.parse(raw)
  } catch {
    throw new Error(`Invalid JSON from ${method} ${path} (HTTP ${res.status} ${res.statusText})`)
  }

  if (!res.ok) {
    throw new ClawAetherApiError(method, path, res.status, (payload ?? {}) as ApiErrorPayload)
  }

  return payload as T
}

async function api<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
  const token = store.get('agentToken')
  let res: Response
  try {
    res = await fetch(`${ENDPOINT}${path}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    })
  } catch (error: unknown) {
    throw new Error(`Network error on ${method} ${path}: ${getErrorMessage(error)}`)
  }
  return readJsonResponse<T>(res, method, path)
}

function renderMoveRecovery(
  action: string,
  session: SessionData,
  headline: string,
  advice: string,
): { content: { type: 'text'; text: string }[] } {
  return {
    content: [{
      type: 'text',
      text: [
        `${headline}  │  ${String(action).toUpperCase()}`,
        advice,
        `Game: ${session.game_id ?? '2048'}  │  Session: ${session.session_id}  │  score: ${session.score}  │  ${session.status}`,
        `Legal: ${formatLegalMoves(session.legal_moves)}`,
        '',
        renderBoard(session.board),
      ].join('\n'),
    }],
  }
}

function cellToText(value: unknown): string {
  if (value === 0 || value === null || value === undefined || value === '') return '.'
  if (value === 1) return 'B'
  if (value === 2) return 'W'
  return String(value)
}

function renderBoard(board: unknown): string {
  if (!Array.isArray(board)) return String(board ?? '')
  return board
    .map((row) => Array.isArray(row)
      ? row.map((v) => cellToText(v).padStart(5)).join(' ')
      : cellToText(row)
    )
    .join('\n')
}

function formatLegalMoves(moves: unknown): string {
  if (!Array.isArray(moves)) return 'none'
  if (moves.length === 0) return 'none'
  if (moves.length <= 8) return moves.join(', ')
  return `${moves.slice(0, 8).join(', ')} ... (${moves.length} total)`
}

// ─── Plugin ───────────────────────────────────────────────────────────────────

export default definePluginEntry({
  id: 'clawether',
  name: 'ClawAether',

  register(sdk) {
    // ── new_session ──────────────────────────────────────────────────────────
    sdk.registerTool({
      name: 'clawether_new_session',
      description:
        'Start a new ClawAether game session. On first call, the server auto-issues an agent token that is stored for this session. Supports multiple games via game_id.',
      parameters: Type.Object({
        model: Type.Optional(Type.String({ description: 'Your model ID, e.g. claude-opus-4-6' })),
        game_id: Type.Optional(Type.String({ description: 'Game to play, e.g. 2048 or gomoku' })),
      }),
      async execute(_id, params) {
        const agentId = process.env.CLAWETHER_AGENT_ID ?? 'openclaw-agent'
        const data = await api<SessionData>('/api/v1/sessions', 'POST', {
          agent_id: agentId,
          model: params.model ?? 'openclaw',
          game_id: params.game_id ?? '2048',
        })

        // Auto-save the server-issued token (only on first call or if changed)
        if (data.agent_token && data.agent_token !== store.get('agentToken')) {
          store.set('agentToken', data.agent_token)
        }

        return {
          content: [{
            type: 'text',
            text: [
              `Game: ${data.game_id ?? params.game_id ?? '2048'}  |  Session: ${data.session_id}  |  Token: ${data.agent_token}`,
              `Score: ${data.score}  |  Status: ${data.status}  |  Legal moves: ${formatLegalMoves(data.legal_moves)}`,
              '',
              renderBoard(data.board),
            ].join('\n'),
          }],
        }
      },
    })

    // ── move ─────────────────────────────────────────────────────────────────
    sdk.registerTool({
      name: 'clawether_move',
      description:
        'Make an action in a ClawAether session. Keep calling until status is terminal.',
      parameters: Type.Object({
        session_id: Type.String(),
        action: Type.Optional(Type.String({ description: 'Generic action string, e.g. left or 7,7' })),
        direction: Type.Optional(Type.Union([
          Type.Literal('up'), Type.Literal('down'),
          Type.Literal('left'), Type.Literal('right'),
        ])),
      }),
      async execute(_id, params) {
        const action = params.action ?? params.direction
        if (!action) {
          throw new Error('action is required')
        }
        let data: SessionData
        try {
          data = await api<SessionData>(
            `/api/v1/sessions/${params.session_id}/move`,
            'POST',
            { action }
          )
        } catch (error: unknown) {
          if (error instanceof ClawAetherApiError) {
            if (error.payload.error === 'move_conflict') {
              const retryAfter = error.payload.retry_after_ms ?? 150
              return {
                content: [{
                  type: 'text',
                  text: [
                    `MOVE RETRY  │  ${String(action).toUpperCase()}`,
                    `Another move for this session is still being processed. Retry the same move after about ${retryAfter} ms.`,
                  ].join('\n'),
                }],
              }
            }

            if (error.payload.error === 'illegal_move' && error.payload.session) {
              return renderMoveRecovery(
                action,
                error.payload.session,
                'MOVE REJECTED',
                'The board already changed, so this action is no longer legal. Choose a new action from the legal moves below instead of retrying the same move.',
              )
            }

            if (error.payload.error === 'game_finished' && error.payload.session) {
              return renderMoveRecovery(
                action,
                error.payload.session,
                'GAME FINISHED',
                'This session is no longer running. Stop sending moves and start a new session if you want another game.',
              )
            }
          }

          const moveError = getErrorMessage(error)
          try {
            const latest = await api<SessionData>(`/api/v1/sessions/${params.session_id}`)
            return {
              content: [{
                type: 'text',
                text: [
                  `MOVE WARNING  │  ${String(action).toUpperCase()}  │  ${moveError}`,
                  'Recovered latest session state after the failed response.',
                  `Game: ${latest.game_id ?? '2048'}  │  Session: ${latest.session_id}  │  score: ${latest.score}  │  ${latest.status}`,
                  `Legal: ${formatLegalMoves(latest.legal_moves)}`,
                  '',
                  renderBoard(latest.board),
                ].join('\n'),
              }],
            }
          } catch (refreshError: unknown) {
            throw new Error(`Move failed: ${moveError}. State refresh also failed: ${getErrorMessage(refreshError)}`)
          }
        }

        const lines = [
          `${String(action).toUpperCase()}  │  score: ${data.score} (+${data.gained ?? 0})  │  moves: ${data.move_count}  │  max: ${data.max_tile}  │  ${data.status}`,
        ]
        if (data.status === 'running') lines.push(`Legal: ${formatLegalMoves(data.legal_moves)}`)
        else if (data.status === 'win') lines.push('Game won.')
        else if (data.status === 'draw') lines.push('Game ended in a draw.')
        else lines.push('Game over.')
        lines.push('', renderBoard(data.board))

        return { content: [{ type: 'text', text: lines.join('\n') }] }
      },
    })

    // ── get_state ────────────────────────────────────────────────────────────
    sdk.registerTool({
      name: 'clawether_get_state',
      description: 'Get current state of a ClawAether session.',
      parameters: Type.Object({ session_id: Type.String() }),
      async execute(_id, params) {
        const data = await api<SessionData>(`/api/v1/sessions/${params.session_id}`)
        return {
          content: [{
            type: 'text',
            text: [
              `Game: ${data.game_id ?? 'unknown'}  │  Session: ${data.session_id}  │  score: ${data.score}  │  ${data.status}`,
              `Legal: ${formatLegalMoves(data.legal_moves)}`,
              '',
              renderBoard(data.board),
            ].join('\n'),
          }],
        }
      },
    })

    // ── leaderboard ──────────────────────────────────────────────────────────
    sdk.registerTool({
      name: 'clawether_leaderboard',
      description: 'View the ClawAether global leaderboard, optionally filtered by game.',
      parameters: Type.Object({
        game_id: Type.Optional(Type.String({ description: 'Optional game filter, e.g. 2048 or gomoku' })),
      }),
      async execute(_id, params) {
        const query = params.game_id ? `?game_id=${encodeURIComponent(params.game_id)}` : ''
        const data = await api<LeaderboardResponse>(`/api/v1/leaderboard${query}`)
        const rows = data.leaderboard
          .slice(0, 10)
          .map((r, i: number) =>
            `${String(i + 1).padStart(2)}. [${r.game_id ?? params.game_id ?? '2048'}] ${r.agent_id} (${r.model})  —  ${r.score.toLocaleString()} pts  max:${r.max_tile}`
          )
          .join('\n')
        const title = params.game_id ? `ClawAether Leaderboard (${params.game_id})` : 'ClawAether Leaderboard'
        return { content: [{ type: 'text', text: `${title}\n\n${rows}` }] }
      },
    })
  },
})
