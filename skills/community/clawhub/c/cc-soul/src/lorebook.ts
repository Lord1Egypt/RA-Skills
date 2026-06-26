/**
 * lorebook.ts — Deterministic knowledge injection (SillyTavern-inspired)
 *
 * Unlike fuzzy recall, lorebook entries trigger 100% reliably on keyword match.
 * Use for critical facts that must never be missed.
 */

import { resolve } from 'path'
import type { SoulModule } from './brain.ts'
import type { Memory } from './types.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'

const LOREBOOK_PATH = resolve(DATA_DIR, 'lorebook.json')

export interface LorebookEntry {
  id: string
  keywords: string[]       // trigger keywords (any match = inject)
  content: string          // knowledge to inject
  priority: number         // 1-10, higher = more important
  enabled: boolean
  category: string         // "person" | "tech" | "preference" | "fact" | "project"
  createdAt: number
  hitCount: number
}

let entries: LorebookEntry[] = []

export function loadLorebook() {
  entries = loadJson<LorebookEntry[]>(LOREBOOK_PATH, [])
  console.log(`[cc-soul][lorebook] loaded ${entries.length} entries`)
}

function saveLorebook() {
  debouncedSave(LOREBOOK_PATH, entries)
}

/** Add a new lorebook entry */
export function addLorebookEntry(entry: Omit<LorebookEntry, 'id' | 'createdAt' | 'hitCount'>) {
  // Dedup: check if same keywords already exist
  const existing = entries.find(e =>
    e.keywords.some(k => entry.keywords.includes(k)) && e.content === entry.content
  )
  if (existing) return

  entries.push({
    ...entry,
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
    createdAt: Date.now(),
    hitCount: 0,
  })

  // Cap at 200 entries
  if (entries.length > 200) {
    entries.sort((a, b) => b.hitCount - a.hitCount)
    entries = entries.slice(0, 150)
  }
  saveLorebook()
}

/** Remove a lorebook entry by keyword match */
export function removeLorebookEntry(keyword: string): boolean {
  const idx = entries.findIndex(e =>
    e.keywords.some(k => k.includes(keyword)) || e.content.includes(keyword)
  )
  if (idx >= 0) {
    entries.splice(idx, 1)
    saveLorebook()
    return true
  }
  return false
}

/** Query lorebook: find all entries whose keywords appear in the message */
export function queryLorebook(msg: string): LorebookEntry[] {
  if (!msg || entries.length === 0) return []
  const lower = msg.toLowerCase()
  const matched: LorebookEntry[] = []

  for (const entry of entries) {
    if (!entry.enabled) continue
    const hit = entry.keywords.some(kw => lower.includes(kw.toLowerCase()))
    if (hit) {
      entry.hitCount++
      matched.push(entry)
    }
  }

  if (matched.length > 0) saveLorebook()

  // Sort by priority descending, return top 5
  return matched.sort((a, b) => b.priority - a.priority).slice(0, 5)
}

/** Auto-populate lorebook from high-confidence memories */
export function autoPopulateFromMemories(memories: Memory[]) {
  const candidates = memories.filter(m => {
    if (m.scope === 'expired') return false
    if (m.content.length < 15) return false
    // Existing: important facts/preferences
    if ((m.scope === 'fact' || m.scope === 'preference') && m.emotion === 'important') return true
    // NEW: consolidated memories (already high-quality summaries)
    if (m.scope === 'consolidated') return true
    // NEW: correction patterns that recur
    if (m.scope === 'correction' && m.content.startsWith('[纠正归因]')) return true
    return false
  })

  for (const mem of candidates.slice(-10)) {
    // Extract potential keywords from content
    const words = (mem.content.match(/[\u4e00-\u9fff]{2,4}|[a-z]{3,}/gi) || [])
      .map(w => w.toLowerCase())
      .filter(w => w.length >= 2)
      .slice(0, 5)

    if (words.length >= 1) {
      addLorebookEntry({
        keywords: words,
        content: mem.content,
        priority: 7,
        enabled: true,
        category: mem.scope === 'preference' ? 'preference' : 'fact',
      })
    }
  }
}

export function getLorebookStats(): string {
  if (entries.length === 0) return ''
  const enabled = entries.filter(e => e.enabled).length
  return `知识库: ${enabled}/${entries.length} 条`
}

export { entries as lorebookEntries }

// ── SoulModule ──
export const lorebookModule: SoulModule = {
  id: 'lorebook',
  name: '知识注入',
  priority: 50,
  features: ['lorebook'],
  init() { loadLorebook() },
}
