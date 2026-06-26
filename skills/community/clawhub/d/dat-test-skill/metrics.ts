#!/usr/bin/env node
// Usage: npx tsx metrics.ts [--cwd=<path>]  |  BRV_CMD=./bin/dev.js npx tsx metrics.ts --cwd=/path/to/project

import { execSync } from 'node:child_process'
import { homedir } from 'node:os'

const BRV = process.env.BRV_CMD ?? 'brv'
const SINCE = process.env.BRV_SINCE ?? '24h'
const QUERY_FETCH_LIMIT = 1000
const CURATE_FETCH_LIMIT = 1000

const cwdArg = process.argv
  .find((a: string) => a.startsWith('--cwd='))
  ?.slice('--cwd='.length)
  .replace(/^~/, homedir())

const QUOTA_PATTERNS = [
  'request limit exceeded',
  "you've reached your",
  'upgrade your plan',
  'err_llm_rate_limit',
  'llm_rate_limit_exceeded',
  'rate limit exceeded',
]

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type QueryLogStatus = 'cancelled' | 'completed' | 'error' | 'processing'
type CurateLogStatus = 'cancelled' | 'completed' | 'error' | 'processing'

type QueryLogEntry = {
  id: string
  startedAt: number
  status: QueryLogStatus
  timing?: { durationMs: number }
  error?: string
}

type CurateLogOperation = {
  type: 'ADD' | 'DELETE' | 'MERGE' | 'UPDATE' | 'UPSERT'
  status: 'failed' | 'success'
}

type CurateLogEntry = {
  id: string
  startedAt: number
  status: CurateLogStatus
  summary: { added: number; deleted: number; failed: number; merged: number; updated: number }
  operations: CurateLogOperation[]
  error?: string
}

type BrvJsonResponse<T> = {
  data: T[]
  success: boolean
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function fetchBrv<T>(subcommand: string, limit: number, since?: string, cwd?: string): T[] {
  const sinceFlag = since ? ` --since=${since}` : ''
  try {
    const raw = execSync(`${BRV} ${subcommand} --format=json --limit=${limit}${sinceFlag}`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe'],
      ...(cwd !== undefined && { cwd }),
    })
    const parsed = JSON.parse(raw) as BrvJsonResponse<T>
    return parsed.data ?? []
  } catch (err) {
    const stdout = err != null && typeof err === 'object' && 'stdout' in err ? String((err as Record<string, unknown>).stdout ?? '') : ''
    const stderr = err != null && typeof err === 'object' && 'stderr' in err ? String((err as Record<string, unknown>).stderr ?? '') : ''
    const message = err instanceof Error ? err.message : String(err)
    if (stdout) {
      try {
        const parsed = JSON.parse(stdout) as BrvJsonResponse<T>
        return parsed.data ?? []
      } catch {
        // stdout not JSON — fall through
      }
    }
    console.error(`  [error] brv ${subcommand}: ${message}`)
    if (stderr.trim()) console.error(`  stderr: ${stderr.trim()}`)
    return []
  }
}

function fetchLogPair<T>(subcommand: string, limit: number, cwd?: string): { recent: T[] } {
  return {
    recent: fetchBrv<T>(subcommand, limit, SINCE, cwd),
  }
}

function isQuotaError(msg: string): boolean {
  const lower = msg.toLowerCase()
  return QUOTA_PATTERNS.some((p) => lower.includes(p))
}

function avg(nums: number[]): number | undefined {
  if (nums.length === 0) return undefined
  return Math.round(nums.reduce((a, b) => a + b, 0) / nums.length)
}

function fmtDuration(ms: number): string {
  if (ms < 1_000) return `${ms} ms`
  if (ms < 60_000) return `${(ms / 1_000).toFixed(1)} s`
  return `${(ms / 60_000).toFixed(1)} min`
}

function row(label: string, value: string | number): void {
  console.log(`  ${label.padEnd(22)} ${value}`)
}

function printQuotaErrors(errors: Array<{ id: string; error?: string }>): void {
  for (const e of errors) {
    console.log(`    → [${e.id}] ${e.error}`)
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main(): void {
  console.log(`\n=== ByteRover Metrics — Last ${SINCE} ===\n`)

  const queryLogs = fetchLogPair<QueryLogEntry>('query-log view', QUERY_FETCH_LIMIT, cwdArg)
  const completedQueries = queryLogs.recent.filter((e) => e.status === 'completed')
  const errorQueries = queryLogs.recent.filter((e) => e.status === 'error')
  const durations = completedQueries.flatMap((e) =>
    e.timing?.durationMs !== undefined ? [e.timing.durationMs] : [],
  )
  const queryQuotaErrors = errorQueries.filter((e) => e.error && isQuotaError(e.error))

  console.log('── Query Logs ────────────────────────────')
  row(`Executed (${SINCE}):`, queryLogs.recent.length)
  row('Completed:', completedQueries.length)
  row('Errors:', errorQueries.length)
  row('Avg retrieval time:', durations.length > 0 ? fmtDuration(avg(durations)!) : 'N/A')
  row('Quota errors:', queryQuotaErrors.length > 0 ? `${queryQuotaErrors.length}  ⚠️` : queryQuotaErrors.length)
  printQuotaErrors(queryQuotaErrors)

  const curateLogs = fetchLogPair<CurateLogEntry>('curate view', CURATE_FETCH_LIMIT, cwdArg)
  const completedCurates = curateLogs.recent.filter((e) => e.status === 'completed')
  const errorCurates = curateLogs.recent.filter((e) => e.status === 'error')
  const totalAdded = completedCurates.reduce((sum, e) => sum + e.summary.added, 0)
  // treat merged as updated — MERGE keeps the file, just updates it
  const totalUpdated = completedCurates.reduce((sum, e) => sum + e.summary.updated + e.summary.merged, 0)
  const curateQuotaErrors = errorCurates.filter((e) => e.error && isQuotaError(e.error))

  console.log('\n── Curate Logs ───────────────────────────')
  row(`Executed (${SINCE}):`, curateLogs.recent.length)
  row('Completed:', completedCurates.length)
  row('Errors:', errorCurates.length)
  row('Files added:', totalAdded)
  row('Files updated/merged:', totalUpdated)
  row('Quota errors:', curateQuotaErrors.length > 0 ? `${curateQuotaErrors.length}  ⚠️` : curateQuotaErrors.length)
  printQuotaErrors(curateQuotaErrors)

  console.log('\n==========================================\n')
}

main()
