import { format } from 'node:util'

const enabled = process.env.CLAUDE_COMPUTER_USE_DEBUG === '1'

export function logDebug(message: string, ...args: unknown[]): void {
  if (!enabled) return
  process.stderr.write(`[claude-computer-use] ${format(message, ...args)}\n`)
}

export function logWarn(message: string, ...args: unknown[]): void {
  process.stderr.write(`[claude-computer-use][warn] ${format(message, ...args)}\n`)
}
