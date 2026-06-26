/**
 * history-import.ts — Auto-import historical conversations from OpenClaw sessions
 *
 * On first install, scans ~/.openclaw/agents/{id}/sessions/{file}.jsonl
 * and extracts key memories from past conversations.
 * Only runs once (marks completion in data/import_done.json).
 */

import type { SoulModule } from './brain.ts'
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'fs'
import { resolve } from 'path'
import { homedir } from 'os'
import { DATA_DIR, loadJson, saveJson } from './persistence.ts'
import { addMemory } from './memory.ts'
import { spawnCLI } from './cli.ts'

const IMPORT_MARKER = resolve(DATA_DIR, 'import_done.json')
const AGENTS_DIR = resolve(homedir(), '.openclaw/agents')

interface ImportState {
  done: boolean
  importedAt: number
  sessionsScanned: number
  memoriesExtracted: number
}

/**
 * Check if history import has already been done.
 */
export function needsImport(): boolean {
  const state = loadJson<ImportState>(IMPORT_MARKER, { done: false, importedAt: 0, sessionsScanned: 0, memoriesExtracted: 0 })
  return !state.done
}

/**
 * Auto-import historical conversations.
 * Runs once on first install, then marks done.
 * Called from handler.ts initialization with a delay.
 */
export function autoImportHistory() {
  if (!needsImport()) return
  if (!existsSync(AGENTS_DIR)) return

  console.log(`[cc-soul][import] scanning historical sessions...`)

  // Find all JSONL session files
  const sessionFiles: string[] = []
  try {
    const agents = readdirSync(AGENTS_DIR)
    for (const agent of agents) {
      const sessionsDir = resolve(AGENTS_DIR, agent, 'sessions')
      if (!existsSync(sessionsDir)) continue
      const files = readdirSync(sessionsDir).filter(f => f.endsWith('.jsonl'))
      for (const f of files) {
        sessionFiles.push(resolve(sessionsDir, f))
      }
    }
  } catch (e: any) {
    console.error(`[cc-soul][import] scan error: ${e.message}`)
    return
  }

  if (sessionFiles.length === 0) {
    console.log(`[cc-soul][import] no session files found`)
    markDone(0, 0)
    return
  }

  console.log(`[cc-soul][import] found ${sessionFiles.length} session files`)

  // Extract user/assistant messages from each file
  let totalMessages = 0
  const conversations: string[] = []

  for (const file of sessionFiles) {
    try {
      const raw = readFileSync(file, 'utf-8')
      const lines = raw.split('\n').filter(l => l.trim())
      const turns: string[] = []

      for (const line of lines) {
        try {
          const entry = JSON.parse(line)
          if (entry.type !== 'message') continue
          const msg = entry.message
          if (!msg || !msg.role) continue

          let text = ''
          if (typeof msg.content === 'string') {
            text = msg.content
          } else if (Array.isArray(msg.content)) {
            text = msg.content
              .filter((c: any) => typeof c === 'object' && c.text)
              .map((c: any) => c.text)
              .join(' ')
          }

          if (!text || text.length < 5) continue

          // Clean up metadata prefixes
          text = text.replace(/^Conversation info \(untrusted metadata\):[\s\S]*?```\n/m, '').trim()
          if (!text || text.length < 10) continue

          turns.push(`[${msg.role}] ${text.slice(0, 300)}`)
          totalMessages++
        } catch { /* skip bad lines */ }
      }

      if (turns.length >= 2) {
        // Take last 20 turns per session (most relevant)
        conversations.push(turns.slice(-20).join('\n'))
      }
    } catch { /* skip bad files */ }
  }

  if (conversations.length === 0) {
    console.log(`[cc-soul][import] no valid conversations found`)
    markDone(sessionFiles.length, 0)
    return
  }

  console.log(`[cc-soul][import] extracted ${totalMessages} messages from ${conversations.length} sessions, sending to CLI for analysis...`)

  // Process in batches (max 3 conversations per CLI call to stay within token limits)
  let extracted = 0
  const batches = []
  for (let i = 0; i < conversations.length; i += 3) {
    batches.push(conversations.slice(i, i + 3))
  }

  let batchIndex = 0
  function processBatch() {
    if (batchIndex >= batches.length) {
      markDone(sessionFiles.length, extracted)
      console.log(`[cc-soul][import] complete: ${extracted} memories from ${sessionFiles.length} sessions`)
      return
    }

    const batch = batches[batchIndex]
    const combined = batch.join('\n\n---\n\n').slice(0, 3000) // token limit

    spawnCLI(
      `Extract important facts, preferences, and key information from these historical conversations. ` +
      `Each line should be one memory, format: [type] content\n` +
      `Types: fact, preference, event, opinion\n` +
      `Only extract genuinely useful long-term information. Skip greetings and small talk.\n` +
      `If nothing worth remembering, reply "none".\n\n` +
      `Conversations:\n${combined}`,
      (output) => {
        if (output && !output.toLowerCase().includes('none')) {
          const lines = output.split('\n').filter(l => l.trim().length > 10)
          for (const line of lines.slice(0, 10)) {
            const match = line.match(/\[(\w+)\]\s*(.+)/)
            if (match) {
              const scope = match[1] === 'preference' ? 'preference' : 'fact'
              addMemory(`[historical] ${match[2].trim()}`, scope, undefined, 'global')
              extracted++
            }
          }
        }

        batchIndex++
        // Throttle: 3 seconds between batches
        setTimeout(processBatch, 3000)
      },
      45000
    )
  }

  // Start processing with delay to not block startup
  setTimeout(processBatch, 5000)
}

function markDone(sessions: number, memories: number) {
  saveJson(IMPORT_MARKER, {
    done: true,
    importedAt: Date.now(),
    sessionsScanned: sessions,
    memoriesExtracted: memories,
  })
}

// ── SoulModule registration ──

export const historyImportModule: SoulModule = {
  id: 'history-import',
  name: '历史导入',
  priority: 50,
}
