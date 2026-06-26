/**
 * handler-heartbeat.ts — cc-soul 自主心跳循环
 *
 * 每 30 分钟执行一次的后台维护任务集合。
 * 从 handler.ts 提取，降低主文件复杂度。
 */

import {
  metrics, stats, getHeartbeatRunning, setHeartbeatRunning,
  getHeartbeatStartedAt, setHeartbeatStartedAt,
} from './handler-state.ts'
import { dbGetDueReminders, dbMarkReminderFired } from './sqlite-store.ts'
import { bodyTick } from './body.ts'
import {
  consolidateMemories, scanForContradictions,
  evaluateAndPromoteMemories, autoPromoteToCoreMemory, cleanupWorkingMemory, processMemoryDecay,
  batchTagUntaggedMemories, auditMemoryHealth,
  sqliteMaintenance,
  pruneExpiredMemories, reviveDecayedMemories,
  compressOldMemories,
} from './memory.ts'
import { cleanupPlans } from './inner-life.ts'
import { computePageRank, decayActivations, invalidateStaleEntities, invalidateStaleRelations, enrichCausalFromMemories } from './graph.ts'
import { isEnabled } from './features.ts'
import { checkAutoTune } from './auto-tune.ts'
import { resampleHardExamples } from './quality.ts'
import { runDistillPipeline } from './distill.ts'
import { healthCheck, recordModuleError, recordModuleActivity } from './health.ts'
import { notifySoulActivity } from './notify.ts'
import { brain } from './brain.ts'
import { distillPersonModel } from './person-model.ts'
import { tickBatchQueue } from './cli.ts'
// person synthesis now handled inside person-model.ts distillPersonModel() (every 5th distill)
import { heartbeatScanAbsence } from './absence-detection.ts'
import { scanBlindSpotQuestions } from './epistemic.ts'
import { updateDeepUnderstand } from './deep-understand.ts'
import { innerState } from './inner-life.ts'

// ── 休眠巩固：三档心跳 ──
function getHeartbeatMode(): 'awake' | 'light_sleep' | 'deep_sleep' {
  const lastActivity = innerState.lastActivityTime || metrics.lastHeartbeat || 0
  const inactive = Date.now() - lastActivity
  if (inactive < 30 * 60_000) return 'awake'
  if (inactive < 6 * 3600_000) return 'light_sleep'
  return 'deep_sleep'
}

// ── CLI concurrency semaphore + 熔断器 ──
let _cliSemaphore = 0
const MAX_CLI_CONCURRENT = 3
// 熔断器：连续失败 3 次 → 停 1 小时。按 CLI 可用性熔断（共享），不按业务操作分
let _cliFailures = 0
let _cliCircuitOpenAt = 0

function safeCLI(name: string, fn: () => void, safeFn: (name: string, fn: () => void) => void) {
  // 熔断检查
  if (_cliFailures >= 3) {
    if (Date.now() - _cliCircuitOpenAt < 3600_000) {
      return  // 熔断中，静默跳过
    }
    // 冷却期过了，半开状态
    console.log(`[cc-soul][heartbeat] CLI circuit half-open, attempting ${name}`)
  }
  if (_cliSemaphore >= MAX_CLI_CONCURRENT) {
    return
  }
  _cliSemaphore++
  safeFn(name, () => {
    try {
      fn()
      if (_cliFailures > 0) { _cliFailures = 0 }  // 成功 → 重置
    } catch (e: any) {
      _cliFailures++
      if (_cliFailures >= 3) {
        _cliCircuitOpenAt = Date.now()
        console.error(`[cc-soul][heartbeat] CLI circuit OPEN (${name}: ${e.message})`)
        try { require('./decision-log.ts').logDecision('circuit_open', 'cli', `failures=${_cliFailures}, ${name}: ${e.message}`) } catch {}
      }
      throw e
    } finally { _cliSemaphore-- }
  })
}

/** Exported for plugin-entry.ts heartbeat interval */
export function runHeartbeat() {
  // Force release if stuck for >25 minutes
  if (getHeartbeatRunning() && getHeartbeatStartedAt() > 0 && Date.now() - getHeartbeatStartedAt() > 25 * 60000) {
    console.error('[cc-soul][heartbeat] force-releasing stuck heartbeat lock (>25min)')
    setHeartbeatRunning(false)
  }
  if (getHeartbeatRunning()) return
  setHeartbeatRunning(true)
  setHeartbeatStartedAt(Date.now())
  metrics.lastHeartbeat = Date.now()
    try {
      const safe = (name: string, fn: () => void | Promise<void>) => {
        try {
          const result = fn()
          if (result && typeof (result as any).then === 'function') {
            // async 函数：await 其 Promise，捕获异步异常
            ;(result as Promise<void>).then(() => recordModuleActivity(name)).catch((e: any) => {
              recordModuleError(name, e.message); console.error(`[cc-soul][heartbeat][${name}] async: ${e.message}`)
            })
          } else {
            recordModuleActivity(name)
          }
        } catch (e: any) { recordModuleError(name, e.message); console.error(`[cc-soul][heartbeat][${name}] ${e.message}`) }
      }

      // ── 三档心跳：awake / light_sleep / deep_sleep ──
      const mode = getHeartbeatMode()
      console.log(`[cc-soul][heartbeat] mode=${mode}`)

      // ══ 所有模式都跑的轻量任务 ══
      safe('bodyTick', () => bodyTick())
      safe('batchTag', () => batchTagUntaggedMemories()) // local extraction, no LLM
      safe('workingCleanup', () => cleanupWorkingMemory())
      safe('brainHeartbeat', () => brain.fire('onHeartbeat'))
      safe('health', () => healthCheck())
      safe('planCleanup', () => cleanupPlans())
      safe('batchQueue', () => tickBatchQueue())
      if (isEnabled('absence_detection')) safe('absenceDetection', () => heartbeatScanAbsence())

      // ── 提醒（用户主动设置的，不能砍）──
      safe('reminders', () => {
        const due = dbGetDueReminders()
        for (const r of due) {
          notifySoulActivity(`[提醒] ${r.msg}`)
          dbMarkReminderFired(r.id)
        }
      })

      if (mode === 'awake') {
        // 用户活跃，跳过重计算，只跑轻量任务
        console.log('[cc-soul][heartbeat] awake mode — light tasks only')
      } else {
        // ══ 浅睡 + 深睡：跑维护任务 ══

        // ── 记忆维护（核心，不调 LLM）──
        safeCLI('consolidate', () => consolidateMemories(), safe)
        safeCLI('contradiction', () => scanForContradictions(), safe)
        safe('memoryPromotion', () => evaluateAndPromoteMemories())
        safe('smartForgetSweep', () => { try { const { smartForgetModule } = require('./smart-forget.ts'); smartForgetModule.onHeartbeat() } catch {} })
        safe('memoryDecay', () => processMemoryDecay())
        safe('bayesDecay', () => { try { require('./confidence-cascade.ts').batchTimeDecay(require('./memory.ts').memoryState.memories) } catch {} })
        safe('aamDecay', () => { try { require('./aam.ts').decayCooccurrence() } catch {} })
        safe('pmiClusters', () => { try { require('./aam.ts').buildPMIClusters() } catch {} })
        safe('pruneExpired', () => pruneExpiredMemories())
        safe('reviveDecayed', () => reviveDecayedMemories())
        safe('memoryAudit', () => auditMemoryHealth())
        safe('compressOld', () => compressOldMemories())
        safe('sqliteMaintenance', () => { sqliteMaintenance().catch(() => {}) }) // intentionally silent — maintenance

        // ── 图谱维护 ──
        safe('pageRank', () => computePageRank())
        safe('activationDecay', () => decayActivations())
        safe('staleEntities', () => invalidateStaleEntities())
        safe('staleRelations', () => invalidateStaleRelations())
        safe('enrichCausal', () => enrichCausalFromMemories())

        // 实体结晶缓存：heartbeat 预计算实体画像写入 attrs
        safe('entityCrystal', async () => {
          try {
            const { graphState, generateEntitySummary } = await import('./graph.ts')
            const now = Date.now()
            for (const entity of graphState.entities) {
              if (entity.invalid_at !== null) continue
              if (entity.mentions < 3) continue  // 提及太少不值得画像
              const lastCrystal = entity.attrs.find((a: string) => a.startsWith('crystal:'))
              const lastTs = lastCrystal ? parseInt(lastCrystal.split('|')[1] || '0') : 0
              if (now - lastTs < 86400000) continue  // <24h 不刷新
              const summary = generateEntitySummary(entity.name)
              if (summary) {
                entity.attrs = entity.attrs.filter((a: string) => !a.startsWith('crystal:'))
                entity.attrs.push(`crystal:${summary.slice(0, 100)}|${now}`)
              }
            }
          } catch {}
        })

        // ── 预测性记忆预热 ──
        safe('predictivePreload', () => {
          try {
            const { getTopPredictions, getTimeSlot } = require('./behavioral-phase-space.ts')
            const topPredictions: { domain: string; probability: number }[] = getTopPredictions(2)
            if (!topPredictions || topPredictions.length === 0 || topPredictions[0].probability < 0.7) return

            const prediction = topPredictions[0]
            const hour = new Date().getHours()
            const currentSlot: string = getTimeSlot()

            const slotRanges: Record<string, [number, number]> = {
              early_morning: [6, 9],
              morning: [9, 12],
              afternoon: [12, 18],
              evening: [18, 23],
              late_night: [23, 6],
            }
            const range = slotRanges[currentSlot]
            if (!range) return

            const inRange = range[0] <= range[1]
              ? (hour >= range[0] - 1 && hour <= range[1] + 1)
              : (hour >= range[0] - 1 || hour <= range[1] + 1)
            if (!inRange) return

            const predictedTopic = prediction.domain
            if (!predictedTopic) return

            const { memoryState } = require('./memory.ts')
            let preheated = 0
            for (const m of memoryState.memories) {
              if (!m || m.scope === 'expired' || m.scope === 'decayed') continue
              if (m.content && m.content.includes(predictedTopic)) {
                m._preheated = true
                m.confidence = Math.min(1.0, (m.confidence || 0.7) + 0.05)
                preheated++
                if (preheated >= 5) break
              }
            }

            if (preheated > 0) {
              console.log(`[cc-soul][heartbeat] pre-heated ${preheated} memories for predicted topic="${predictedTopic}" (conf=${prediction.probability.toFixed(2)})`)
              try { require('./decision-log.ts').logDecision('preheat', predictedTopic, `${preheated} memories, conf=${prediction.probability.toFixed(2)}, slot=${currentSlot}`) } catch {}
            }
          } catch {}
        })

        // ── 其他维护 ──
        if (isEnabled('self_upgrade')) safe('autoTune', () => checkAutoTune(stats))
        safeCLI('qualityResample', () => resampleHardExamples(), safe)
        safe('blindSpotQuestions', () => scanBlindSpotQuestions())
        safe('deepUnderstand', () => updateDeepUnderstand())

        // ── 动态结构词发现 ──
        safe('structureWordDiscovery', async () => {
          try {
            const { discoverNewStructureWords } = await import('./dynamic-extractor.ts')
            const { getSessionState, getLastActiveSessionKey } = await import('./handler-state.ts')
            const sess = getSessionState(getLastActiveSessionKey())
            const userId = sess?.userId || 'default'
            discoverNewStructureWords(userId)
          } catch {}
        })

        // ── 行为模式学习 ──
        safe('behaviorLearn', async () => {
          const { learnFromObservations } = await import('./behavioral-phase-space.ts')
          learnFromObservations()
        })

        // ── 前瞻记忆清理 + 主动发现 ──
        safe('pmCleanup', async () => {
          const { cleanupProspectiveMemories, autoDetectFromMemories } = await import('./prospective-memory.ts')
          cleanupProspectiveMemories()
          try {
            const { memoryState } = await import('./memory.ts')
            if (memoryState.memories.length > 0) {
              autoDetectFromMemories(memoryState.memories)
            }
          } catch {}
        })


        if (mode === 'deep_sleep') {
          // ══ 深睡：跑全量重计算 ══
          console.log('[cc-soul][heartbeat] deep_sleep mode — full consolidation')
          safeCLI('distill', () => runDistillPipeline(), safe)
          safeCLI('personModel', () => distillPersonModel(), safe)

          // ── 记忆结晶：从行为模式 + 进化规则中提炼抽象性格特征 ──
          safe('crystallize', async () => {
            const { crystallizeTraits } = await import('./person-model.ts')
            crystallizeTraits()
          })

          // ── Skill Memory 提炼（MemOS 启发）──
          safe('skillExtract', async () => {
            try {
              const { traceCausalChain, graphState } = await import('./graph.ts')
              const { memoryState } = await import('./memory.ts')
              const { DATA_DIR, loadJson, debouncedSave } = await import('./persistence.ts')
              const { resolve } = await import('path')

              const SKILLS_PATH = resolve(DATA_DIR, 'skills.json')
              interface Skill { id: string; trigger: string[]; steps: string[]; learnedFrom: string[]; successRate: number; lastUsed: number; domain: string }
              let skills: Skill[] = loadJson<Skill[]>(SKILLS_PATH, [])
              if (skills.length >= 50) return  // 技能上限

              const resolvedEpisodes = memoryState.memories.filter((m: any) =>
                m && m.scope === 'event' && /解决|搞定|成功|修好/.test(m.content)
              ).slice(-10)

              for (const resolved of resolvedEpisodes) {
                const entities = (await import('./graph.ts')).findMentionedEntities(resolved.content)
                if (entities.length === 0) continue
                const chain = traceCausalChain(entities.slice(0, 1), 2)
                if (chain.length === 0) continue

                const trigger = entities.slice(0, 2)
                const steps = chain.map((c: string) => c.slice(0, 50))
                const id = `skill_${Date.now()}_${Math.random().toString(36).slice(2,5)}`

                const hasSimilar = skills.some(s => s.trigger.some(t => trigger.includes(t)))
                if (hasSimilar) continue

                skills.push({ id, trigger, steps, learnedFrom: [resolved.content.slice(0, 40)], successRate: 0.5, lastUsed: 0, domain: entities[0] })
              }

              try {
                const { getRules } = await import('./evolution.ts')
                const rules = getRules?.() ?? []
                for (const r of rules.filter((r: any) => r.hits >= 5 && r.hits / (r.hits + (r.misses ?? 0) + 1) > 0.7)) {
                  const trigger = (r.conditions ?? []).slice(0, 3)
                  if (trigger.length === 0) continue
                  const hasSimilar = skills.some(s => s.trigger.some(t => trigger.includes(t)))
                  if (hasSimilar) continue
                  skills.push({
                    id: `skill_rule_${Date.now()}_${Math.random().toString(36).slice(2,5)}`,
                    trigger, steps: [r.rule], learnedFrom: [r.source ?? 'evolution'],
                    successRate: r.hits / (r.hits + (r.misses ?? 0) + 1), lastUsed: 0, domain: trigger[0],
                  })
                }
              } catch {}

              if (skills.length > 50) skills = skills.slice(-50)
              debouncedSave(SKILLS_PATH, skills, 5000)
            } catch {}
          })
        }
      }
    } catch (e: any) {
      console.error(`[cc-soul][heartbeat] ${e.message}`)
    } finally {
      setHeartbeatRunning(false)
    }
}
