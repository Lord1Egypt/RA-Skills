/**
 * soul-proactive.ts — Automatic insight generation
 *
 * Generates proactive hints (care/followup/relationship/insight) that get
 * injected into augments naturally. NOT sent as messages — AI decides
 * whether to mention them during conversation.
 */

import './persistence.ts' // ensure data dir init

export { generateProactiveItems }
export type { ProactiveItem }

interface ProactiveItem {
  type: string       // 'care' | 'followup' | 'milestone' | 'insight' | 'relationship' | 'revival'
  message: string
  priority: number   // 1-10
  userId?: string
  createdAt: number
}

let lastCheck = 0
const COOLDOWN = 10 * 60 * 1000  // 10 min

async function generateProactiveItems(): Promise<ProactiveItem[]> {
  const now = Date.now()
  if (now - lastCheck < COOLDOWN) return []
  lastCheck = now

  const userId = 'default'
  const items: ProactiveItem[] = []

  // ── 1. Mood care ──
  try {
    const { loadJson, DATA_DIR } = await import('./persistence.ts')
    const { resolve } = await import('path')
    const moodHistory: any[] = loadJson(resolve(DATA_DIR, 'mood_history.json'), [])
    const recent = moodHistory.filter(m => now - m.ts < 3 * 24 * 3600_000)
    const avgMood = recent.length > 0 ? recent.reduce((s, m) => s + (m.mood || 0), 0) / recent.length : 0
    if (avgMood < -0.3 && recent.length >= 3) {
      items.push({ type: 'care', message: '用户最近情绪偏低落，回复时多一些关怀和理解', priority: 9, userId, createdAt: now })
    }
  } catch {}

  // ── 2. Follow-ups ──
  try {
    const { peekPendingFollowUps } = await import('./inner-life.ts')
    for (const fu of peekPendingFollowUps().slice(0, 2)) {
      items.push({ type: 'followup', message: `可以自然地问一下：${fu}`, priority: 7, userId, createdAt: now })
    }
  } catch {}

  // ── 3. Goal milestones ──
  try {
    const { getDb } = await import('./sqlite-store.ts')
    const db = getDb()
    if (db) {
      const goals = db.prepare?.('SELECT * FROM goals WHERE progress >= 50 AND progress < 100')?.all?.() || []
      for (const g of (goals as any[])) {
        items.push({ type: 'milestone', message: `用户的目标"${g.description}"已完成 ${g.progress}%`, priority: 6, userId, createdAt: now })
      }
    }
  } catch {}

  // ── 4. Behavior insights ──
  try {
    const { getProfile } = await import('./user-profiles.ts')
    const profile = getProfile(userId)
    if (profile?.rhythm && profile.messageCount > 50) {
      const hours = profile.rhythm.activeHours || []
      const peak = hours.indexOf(Math.max(...hours))
      if (peak >= 0) {
        const now_h = new Date().getHours()
        if (Math.abs(now_h - peak) > 6) {
          items.push({ type: 'insight', message: `用户通常在 ${peak}:00 最活跃，现在不是他的活跃时段`, priority: 4, userId, createdAt: now })
        }
      }
    }
  } catch {}

  // ── 5. Relationship alerts ──
  try {
    const { loadAvatarProfile } = await import('./avatar.ts')
    const profile = loadAvatarProfile(userId)
    for (const [name, contact] of Object.entries(profile.social || {})) {
      const sc = contact as any
      if (sc.samples?.length >= 5) {
        const allSamples = [...(profile.expression.samples?.casual || []), ...(profile.expression.samples?.technical || []), ...(profile.expression.samples?.emotional || []), ...(profile.expression.samples?.general || [])]
        const recentMentions = allSamples.filter((s: string) => s.includes(name)).length
        if (recentMentions === 0) {
          items.push({ type: 'relationship', message: `用户最近没提到${name}（${sc.relation}）`, priority: 5, userId, createdAt: now })
        }
      }
    }
  } catch {}

  // ── 6. Memory revival ──
  try {
    const { getMemoriesByScope } = await import('./memory.ts')
    const wisdoms = getMemoriesByScope('wisdom') || []
    const old = wisdoms.filter((m: any) => now - (m.createdAt || 0) > 30 * 24 * 3600_000 && (m.recallCount || 0) < 2)
    if (old.length > 0) {
      const pick = old[Math.floor(Math.random() * old.length)]
      items.push({ type: 'revival', message: `用户之前说过："${pick.content.replace(/^\[.*?\]\s*/, '').slice(0, 50)}"`, priority: 3, userId, createdAt: now })
    }
  } catch {}

  // Dedup by type, sort by priority
  const seen = new Set<string>()
  return items.filter(i => { if (seen.has(i.type)) return false; seen.add(i.type); return true })
    .sort((a, b) => b.priority - a.priority).slice(0, 5)
}
