/**
 * command-core.ts — Shared command logic used by both handler-commands.ts and plugin-commands.ts
 *
 * Each function returns a plain string (the formatted response).
 * Framework-specific routing (cmdReply, replySender, registerCommand) stays in the caller.
 */

import { resolve } from 'path'

import { DATA_DIR, loadJson } from './persistence.ts'
import { memoryState, recall, queryMemoryTimeline } from './memory.ts'
import { stats } from './handler-state.ts'
import { body } from './body.ts'
import { getActivePersona } from './persona.ts'
import { brain } from './brain.ts'
import { getDb } from './sqlite-store.ts'

// ── Helpers ──

/** Read memories from JSON file (guaranteed fresh, no module instance issues) */
function readMemoriesFromDisk(): any[] {
  try {
    const memPath = resolve(DATA_DIR, 'memories.json')
    return loadJson(memPath, [] as any[])
  } catch (_) {}
  return memoryState.memories || []
}

function recallWithFallback(keyword: string, limit: number, senderId?: string): any[] {
  let results = recall(keyword, limit, senderId)
  if (results.length === 0) {
    const allMems = readMemoriesFromDisk()
    const kw = keyword.toLowerCase()
    results = allMems.filter((m: any) =>
      m.scope !== 'expired' && m.scope !== 'decayed' &&
      (m.content.toLowerCase().includes(kw) ||
       (m.tags && m.tags.some((t: string) => t.toLowerCase().includes(kw))))
    ).slice(0, limit)
  }
  // Fallback: SQLite direct query
  if (results.length === 0) {
    try {
      const _sdb = getDb()
      if (_sdb) {
        const kw = `%${keyword.toLowerCase()}%`
        const rows = _sdb.prepare(
          "SELECT content, scope, tags, ts FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?) ORDER BY ts DESC LIMIT ?"
        ).all(kw, kw, limit) as any[]
        results = rows.map((r: any) => ({
          content: r.content,
          scope: r.scope,
          tags: r.tags ? (typeof r.tags === 'string' ? JSON.parse(r.tags) : r.tags) : [],
          ts: r.ts,
        }))
      }
    } catch (_) {}
  }
  return results
}

// ── Exported core command functions ──

/**
 * Search memories by keyword. Returns formatted result string.
 */
export function executeSearch(keyword: string, senderId?: string): string {
  if (!keyword) return '用法: 搜索记忆 <关键词>'
  const results = recallWithFallback(keyword, 10, senderId)
  if (results.length === 0) return `没有找到关于「${keyword}」的记忆。`
  const lines = results.map((m: any, i: number) => {
    const ago = Math.floor((Date.now() - m.ts) / 86400000)
    const agoStr = ago === 0 ? '今天' : `${ago}天前`
    const emotionStr = m.emotion && m.emotion !== 'neutral' ? ` (${m.emotion})` : ''
    return `${i + 1}. [${m.scope}] ${m.content.slice(0, 80)}${emotionStr}（${agoStr}）`
  })
  return `搜索「${keyword}」的记忆结果（${results.length} 条）：\n${lines.join('\n')}`
}

/**
 * List recent memories. Returns formatted result string.
 */
export function executeMyMemories(senderId?: string): string {
  // Try SQLite first (official source)
  try {
    const _sdb = getDb()
    if (_sdb) {
      const activeCount = (_sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed'").get() as any)?.c || 0
      const recent = _sdb.prepare(
        "SELECT scope, content, ts FROM memories WHERE scope != 'expired' AND scope != 'decayed' ORDER BY ts DESC LIMIT 20"
      ).all() as any[]
      if (recent.length > 0) {
        const lines = recent.map((m: any, i: number) => {
          const ago = Math.floor((Date.now() - (m.ts || 0)) / 86400000)
          const agoStr = ago === 0 ? '今天' : `${ago}天前`
          return `${i + 1}. [${m.scope}] ${(m.content || '').slice(0, 60)}（${agoStr}）`
        })
        return `最近记忆（共 ${activeCount} 条活跃）：\n${lines.join('\n')}`
      }
    }
  } catch (_) {}

  // Fallback: JSON file
  const mems = readMemoriesFromDisk()
  const active = mems.filter((m: any) => m.scope !== 'expired' && m.scope !== 'decayed')
  const filtered = active
    .filter((m: any) => !senderId || !m.userId || m.userId === senderId)
    .sort((a: any, b: any) => (b.ts || 0) - (a.ts || 0))
    .slice(0, 20)
  const total = active.filter((m: any) => !senderId || !m.userId || m.userId === senderId).length
  if (filtered.length === 0) return '还没有记忆。'
  const lines = filtered.map((m: any, i: number) => {
    const ago = Math.floor((Date.now() - (m.ts || 0)) / 86400000)
    const agoStr = ago === 0 ? '今天' : `${ago}天前`
    return `${i + 1}. [${m.scope}] ${m.content.slice(0, 60)}（${agoStr}）`
  })
  return `最近记忆（共 ${total} 条活跃）：\n${lines.join('\n')}`
}

/**
 * Stats dashboard. Returns formatted result string.
 */
export function executeStats(): string {
  let active = 0
  try {
    const _sdb = getDb()
    if (_sdb) {
      active = (_sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed'").get() as any)?.c || 0
    }
  } catch (_) {}
  if (active === 0) {
    const mems = readMemoriesFromDisk()
    active = mems.filter((m: any) => m.scope !== 'expired' && m.scope !== 'decayed').length
  }
  const days = stats.firstSeen ? Math.max(1, Math.floor((Date.now() - stats.firstSeen) / 86400000)) : 0
  return `cc-soul 仪表盘
━━━━━━━━━━━━━━━
互动: ${stats.totalMessages} 次 | 认识: ${days} 天
纠正率: ${stats.totalMessages > 0 ? (stats.corrections / stats.totalMessages * 100).toFixed(1) : 0}%
记忆: ${active} 条活跃
模块: ${brain.listModules().length} 个
人格: ${getActivePersona()?.name || 'default'}
能量: ${(body.energy * 100).toFixed(0)}% | 心情: ${(body.mood * 100).toFixed(0)}%`
}

/**
 * Memory health report. Returns formatted result string.
 */
export function executeHealth(): string {
  // Try SQLite first
  try {
    const _sdb = getDb()
    if (_sdb) {
      const total = (_sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed'").get() as any)?.c || 0
      const scopes = _sdb.prepare(
        "SELECT scope, COUNT(*) as c FROM memories WHERE scope != 'expired' AND scope != 'decayed' GROUP BY scope ORDER BY c DESC LIMIT 10"
      ).all() as any[]
      const scopeLines = scopes.map((s: any) => `  ${s.scope}: ${s.c}`).join('\n')

      const highConf = (_sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE confidence >= 0.7 AND scope != 'expired'").get() as any)?.c || 0
      const medConf = (_sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE confidence >= 0.4 AND confidence < 0.7 AND scope != 'expired'").get() as any)?.c || 0
      const lowConf = (_sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE confidence >= 0 AND confidence < 0.4 AND scope != 'expired'").get() as any)?.c || 0
      const cutoff30d = Date.now() - 30 * 86400000
      const decayedCount = (_sdb.prepare("SELECT COUNT(*) as c FROM memories WHERE ts < ? AND recallCount = 0 AND scope != 'expired' AND scope != 'decayed'").get(cutoff30d) as any)?.c || 0

      return [
        `记忆健康报告`,
        `总数: ${total}`,
        ``,
        `Scope 分布:`,
        scopeLines,
        ``,
        `置信度分布:`,
        `  高 (>=0.7): ${highConf}`,
        `  中 (0.4-0.7): ${medConf}`,
        `  低 (<0.4): ${lowConf}`,
        ``,
        `衰减概况:`,
        `  30天以上零命中: ${decayedCount} 条 (${total > 0 ? (decayedCount / total * 100).toFixed(1) : 0}%)`,
        `  活跃记忆: ${total - decayedCount} 条`,
      ].join('\n')
    }
  } catch (_) {}

  // Fallback: JSON file
  const mems = readMemoriesFromDisk()
  const active = mems.filter((m: any) => m.scope !== 'expired' && m.scope !== 'decayed')
  const scopes = new Map<string, number>()
  for (const m of active) {
    const s = m.scope || 'unknown'
    scopes.set(s, (scopes.get(s) || 0) + 1)
  }
  const tagged = active.filter((m: any) => m.tags && m.tags.length > 0).length
  return [
    `记忆健康报告`,
    `总记忆: ${mems.length} | 活跃: ${active.length} | 已标签: ${tagged}`,
    `\n按类型:`,
    ...[...scopes.entries()].sort((a, b) => b[1] - a[1]).map(([s, c]) => `  ${s}: ${c}`),
  ].join('\n')
}

/**
 * Feature status list. Returns formatted result string.
 */
export function executeFeatures(): string {
  try {
    const featPath = resolve(DATA_DIR, 'features.json')
    const feats = loadJson(featPath, {})
    const lines = Object.entries(feats)
      .sort(([, a], [, b]) => (b ? 1 : 0) - (a ? 1 : 0))
      .map(([k, v]) => `${v ? '✅' : '❌'} ${k}`)
    return `功能状态（${lines.length} 项）：\n${lines.join('\n')}`
  } catch (_) {
    return '无法读取功能状态。'
  }
}

/**
 * Memory timeline for a keyword. Returns formatted result string.
 */
export function executeTimeline(keyword: string): string {
  if (!keyword) return '用法: 记忆时间线 <关键词>'
  try {
    const timeline = queryMemoryTimeline(keyword)
    if (!timeline || timeline.length === 0) return `没有找到「${keyword}」的历史记录。`
    return `「${keyword}」记忆时间线：\n${timeline.join('\n')}`
  } catch (_) {
    return '查询失败。'
  }
}
