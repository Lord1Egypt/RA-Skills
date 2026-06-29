/**
 * Optional NDJSON debug logger. Never logs secrets/PII.
 * Enabled only when CLAWBBA_DEBUG=1. Log path is always under the user home dir.
 */
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const SESSION_ID = '8f862e'
const DEBUG_ENABLED = /^(1|true|yes)$/i.test(String(process.env.CLAWBBA_DEBUG || ''))

function resolveLogPath() {
  const custom = String(process.env.CLAWBBA_DEBUG_LOG_PATH || '').trim()
  const candidates = [
    custom || null,
    path.join(os.homedir(), '.openclaw', 'clawbba-debug.log'),
    path.join(os.tmpdir(), 'clawbba-debug.log'),
  ].filter(Boolean)
  for (const p of candidates) {
    try {
      fs.mkdirSync(path.dirname(p), { recursive: true })
      fs.appendFileSync(p, '')
      return p
    } catch {
      /* try next */
    }
  }
  return candidates[0]
}

const LOG_PATH = resolveLogPath()

/** @param {{ hypothesisId?: string, location: string, message: string, data?: Record<string, unknown>, runId?: string }} entry */
export function clawbbaDebugLog(entry) {
  if (!DEBUG_ENABLED) return
  const line = JSON.stringify({
    sessionId: SESSION_ID,
    timestamp: Date.now(),
    ...entry,
  })
  try {
    fs.appendFileSync(LOG_PATH, `${line}\n`)
  } catch {
    /* ignore */
  }
}

export function clawbbaDebugLogPath() {
  return LOG_PATH
}
