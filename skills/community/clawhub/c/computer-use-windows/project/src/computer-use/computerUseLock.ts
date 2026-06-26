import { mkdir, readFile, unlink, writeFile } from 'node:fs/promises'
import { join } from 'node:path'
import { homedir } from 'node:os'
import { getErrnoCode } from '../lib/errors.js'
import { logDebug } from '../lib/log.js'

const LOCK_FILENAME = 'computer-use.lock'
const CONFIG_DIR = join(homedir(), '.windows-computer-use-skill')

let heldLocally = false

export type AcquireResult =
  | { kind: 'acquired'; fresh: boolean }
  | { kind: 'blocked'; by: string }

export type CheckResult =
  | { kind: 'free' }
  | { kind: 'held_by_self' }
  | { kind: 'blocked'; by: string }

function getSessionId(): string {
  return process.env.CODEX_THREAD_ID ?? `pid-${process.pid}`
}

function getLockPath(): string {
  return join(CONFIG_DIR, LOCK_FILENAME)
}

async function readLock(): Promise<{ sessionId: string; pid: number } | undefined> {
  try {
    const parsed = JSON.parse(await readFile(getLockPath(), 'utf8'))
    if (typeof parsed?.sessionId === 'string' && typeof parsed?.pid === 'number') return parsed
  } catch {}
  return undefined
}

function isProcessRunning(pid: number): boolean {
  try {
    process.kill(pid, 0)
    return true
  } catch {
    return false
  }
}

async function tryCreateExclusive(lock: { sessionId: string; pid: number }): Promise<boolean> {
  try {
    await writeFile(getLockPath(), JSON.stringify(lock), { flag: 'wx' })
    return true
  } catch (error) {
    if (getErrnoCode(error) === 'EEXIST') return false
    throw error
  }
}

export async function checkComputerUseLock(): Promise<CheckResult> {
  const existing = await readLock()
  if (!existing) return { kind: 'free' }
  if (existing.sessionId === getSessionId()) return { kind: 'held_by_self' }
  if (isProcessRunning(existing.pid)) return { kind: 'blocked', by: existing.sessionId }
  await unlink(getLockPath()).catch(() => {})
  return { kind: 'free' }
}

export async function tryAcquireComputerUseLock(): Promise<AcquireResult> {
  const lock = { sessionId: getSessionId(), pid: process.pid }
  await mkdir(CONFIG_DIR, { recursive: true })
  if (await tryCreateExclusive(lock)) {
    heldLocally = true
    return { kind: 'acquired', fresh: true }
  }
  const existing = await readLock()
  if (!existing) {
    await unlink(getLockPath()).catch(() => {})
    if (await tryCreateExclusive(lock)) {
      heldLocally = true
      return { kind: 'acquired', fresh: true }
    }
    return { kind: 'blocked', by: 'unknown' }
  }
  if (existing.sessionId === lock.sessionId) {
    heldLocally = true
    return { kind: 'acquired', fresh: false }
  }
  if (isProcessRunning(existing.pid)) return { kind: 'blocked', by: existing.sessionId }
  logDebug('recovering stale computer-use lock from %s', existing.sessionId)
  await unlink(getLockPath()).catch(() => {})
  if (await tryCreateExclusive(lock)) {
    heldLocally = true
    return { kind: 'acquired', fresh: true }
  }
  return { kind: 'blocked', by: 'unknown' }
}

export async function releaseComputerUseLock(): Promise<boolean> {
  const existing = await readLock()
  heldLocally = false
  if (!existing || existing.sessionId !== getSessionId()) return false
  try {
    await unlink(getLockPath())
    return true
  } catch {
    return false
  }
}

export function isLockHeldLocally(): boolean {
  return heldLocally
}
