/**
 * OpenClaw API 类型声明
 */

declare module 'openclaw' {
  export interface SpawnOptions {
    runtime: 'subagent' | 'acp'
    agentId?: string
    task: string
    thinking?: 'low' | 'medium' | 'high'
    mode?: 'run' | 'session'
    cwd?: string
  }

  export interface SpawnResult {
    sessionKey: string
    status: 'running' | 'completed' | 'failed'
  }

  export interface HistoryOptions {
    sessionKey: string
    limit?: number
  }

  export interface HistoryResult {
    messages: Array<{
      role: string
      content: string
      timestamp: Date
    }>
  }

  export interface SendOptions {
    sessionKey: string
    message: string
  }

  export function sessions_spawn(options: SpawnOptions): Promise<SpawnResult>
  export function sessions_history(options: HistoryOptions): Promise<HistoryResult>
  export function sessions_send(options: SendOptions): Promise<void>
}
