/**
 * handler-commands.ts — 命令路由（40+ 命令）
 *
 * 从 handler.ts 提取所有命令处理逻辑。
 * 导出 routeCommand()：返回 true 表示命令已处理（handler.ts 应 return）。
 *
 * v2: 声明式注册表模式 — 每个命令是 SoulCommand 对象，
 *     routeCommand / routeCommandDirect 通过 matchCommand() 统一匹配。
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync } from 'fs'
import { exec } from 'child_process'
import { homedir } from 'os'
import { resolve } from 'path'

import type { SessionState } from './handler-state.ts'
import {
  stats, formatMetrics, shortcuts,
  getPrivacyMode, setPrivacyMode, saveStats,
  getCompressionRate,
  getSoulMode, setSoulMode,
} from './handler-state.ts'
import { loadJson, saveJson, debouncedSave, DATA_DIR } from './persistence.ts'
// audit.ts removed
import { dbAddContextReminder, dbGetContextReminders, getDb } from './sqlite-store.ts'
import { handleFeatureCommand } from './features.ts'
// embedder.ts removed — vector search retired
import {
  memoryState, recall, addMemory, addMemoryWithEmotion, saveMemories,
  queryMemoryTimeline, ensureMemoriesLoaded, restoreArchivedMemories,
  trigrams, trigramSimilarity,
} from './memory.ts'
import { generateMoodReport, formatEmotionAnchors } from './body.ts'
import { getCapabilityScore } from './epistemic.ts'
// user-dashboard.ts 已删除（A2A/MCP/Dashboard 清理）
const handleDashboardCommand = () => '该功能已停用'
const generateMemoryMapHTML = () => ''
const generateDashboardHTML = () => ''
// ── Optional modules (absent in public build) ──
let _exportEvolutionAssets: ((stats: any) => { data: any; path: string }) | null = null
let _importEvolutionAssets: ((filePath: string) => { rulesAdded: number; hypothesesAdded: number }) | null = null
import('./evolution.ts').then(m => { _exportEvolutionAssets = m.exportEvolutionAssets; _importEvolutionAssets = m.importEvolutionAssets }).catch((e: any) => { console.error(`[cc-soul] module load failed (evolution): ${e.message}`) })
// ── End optional modules ──
// A/B experiment retired — startExperiment removed
import { handleTuneCommand } from './auto-tune.ts'
import { ingestFile } from './rag.ts'
import { innerState } from './inner-life.ts'
import { getAllValues } from './values.ts'
import { PERSONAS, getActivePersona } from './persona.ts'
import { checkTaskConfirmation } from './tasks.ts'
import { replySender } from './notify.ts'
import { executeSearch, executeMyMemories, executeStats, executeHealth, executeFeatures, executeTimeline } from './command-core.ts'
// ── Optional modules ──
let getCostSummary: () => string = () => '成本追踪模块未加载'
import('./cost-tracker.ts').then(m => { getCostSummary = m.getCostSummary }).catch((e: any) => { console.error(`[cc-soul] module load failed (cost-tracker): ${e.message}`) })

// ── Command dedup: prevent double replies from inbound_claim + hooks ──
let _lastDirectCmd = { content: '', ts: 0 }
export function wasHandledByDirect(msg: string): boolean {
  return _lastDirectCmd.content === msg.trim() && Date.now() - _lastDirectCmd.ts < 8000
}
function markHandledByDirect(msg: string) {
  _lastDirectCmd = { content: msg.trim(), ts: Date.now() }
}

// ── Full backup / restore helpers ──
function _sanitize(obj: any): any {
  const s = JSON.stringify(obj)
    .replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '[REDACTED]')
    .replace(/\b(?:sk-|api[_-]?key|token|secret|password)[=:]\s*\S+/gi, '[REDACTED]')
  return JSON.parse(s)
}
function _readJson(p: string): any { return loadJson(p, null) }
function _fullBackup(): { path: string; counts: Record<string, number> } {
  const d = DATA_DIR + '/export'; if (!existsSync(d)) mkdirSync(d, { recursive: true })
  const files: Record<string, string> = {
    memories: 'memories.json', rules: 'rules.json', hypotheses: 'hypotheses.json',
    personModel: 'user_model.json', values: 'values.json', features: 'features.json',
    coreMemories: 'core_memories.json', userProfiles: 'user_profiles.json',
    theoryOfMind: 'theory_of_mind.json', body: 'body_state.json',
    emotionAnchors: 'emotion_anchors.json', graph: 'graph.json',
    lorebook: 'lorebook.json',
    journal: 'journal.json', workflows: 'workflows.json', plans: 'plans.json',
  }
  const bundle: Record<string, any> = { _meta: { version: 1, exportedAt: new Date().toISOString(), source: 'cc-soul' } }
  const counts: Record<string, number> = {}
  for (const [key, file] of Object.entries(files)) {
    const raw = _readJson(resolve(DATA_DIR, file))
    if (raw != null) { bundle[key] = raw; counts[key] = Array.isArray(raw) ? raw.length : Object.keys(raw).length }
  }
  // avatar profiles (per-user directory)
  const apDir = resolve(DATA_DIR, 'avatar_profiles')
  if (existsSync(apDir)) {
    const ap: Record<string, any> = {}
    for (const f of readdirSync(apDir).filter(f => f.endsWith('.json'))) {
      const d2 = _readJson(resolve(apDir, f)); if (d2) ap[f.replace('.json', '')] = d2
    }
    if (Object.keys(ap).length) { bundle.avatarProfiles = ap; counts.avatarProfiles = Object.keys(ap).length }
  }
  const sanitized = _sanitize(bundle)
  const ts = new Date().toISOString().slice(0, 10)
  const outPath = `${d}/full_backup_${ts}.json`
  writeFileSync(outPath, JSON.stringify(sanitized, null, 2), 'utf-8')
  return { path: outPath, counts }
}
function _fullRestore(filePath: string): Record<string, number> {
  const raw = JSON.parse(readFileSync(filePath, 'utf-8'))
  if (!raw._meta?.source) throw new Error('不是有效的 cc-soul 全量备份文件')
  const fileMap: Record<string, string> = {
    memories: 'memories.json', rules: 'rules.json', hypotheses: 'hypotheses.json',
    personModel: 'user_model.json', values: 'values.json', features: 'features.json',
    coreMemories: 'core_memories.json', userProfiles: 'user_profiles.json',
    theoryOfMind: 'theory_of_mind.json', body: 'body_state.json',
    emotionAnchors: 'emotion_anchors.json', graph: 'graph.json',
    lorebook: 'lorebook.json',
    journal: 'journal.json', workflows: 'workflows.json', plans: 'plans.json',
  }
  const counts: Record<string, number> = {}
  for (const [key, file] of Object.entries(fileMap)) {
    if (raw[key] != null) {
      writeFileSync(resolve(DATA_DIR, file), JSON.stringify(raw[key], null, 2), 'utf-8')
      counts[key] = Array.isArray(raw[key]) ? raw[key].length : Object.keys(raw[key]).length
    }
  }
  if (raw.avatarProfiles) {
    const apDir = resolve(DATA_DIR, 'avatar_profiles')
    if (!existsSync(apDir)) mkdirSync(apDir, { recursive: true })
    for (const [uid, data] of Object.entries(raw.avatarProfiles)) {
      saveJson(resolve(apDir, `${uid}.json`), data)
    }
    counts.avatarProfiles = Object.keys(raw.avatarProfiles).length
  }
  return counts
}

// ── Command reply helper ──
// Uses OpenClaw SDK (replySender) to send command results directly.
// cfg is threaded through from inbound_claim hook or falls back to legacy path.
let _replyCfg: any = null   // set by handleCommandInbound / setReplyCfg
function setReplyCfg(cfg: any) { _replyCfg = cfg }

function cmdReply(ctx: any, event: any, session: SessionState, text: string, userMsg: string) {
  session.lastPrompt = userMsg
  console.log(`[cc-soul][cmdReply] sending reply (${text.length} chars): ${text.slice(0, 50)}...`)
  // Store reply text in ctx so API callers can retrieve it
  if (typeof ctx.reply === 'function') ctx.reply(text)
  // Determine recipient address
  const evCtx = event?.context || {}
  const to = event?._replyTo || evCtx.conversationId || evCtx.chatId || ''
  replySender(to, text, _replyCfg || event?._replyCfg)
    .then(() => console.log(`[cc-soul][cmdReply] sent OK`))
    .catch((e: any) => console.error(`[cc-soul][cmdReply] failed: ${e.message}`))
  // Minimal bodyForAgent to prevent AI from answering the command again
  ctx.bodyForAgent = '[系统] 命令已处理，结果已发送。'
}

// ═══════════════════════════════════════════════════════════════════════════════
// DECLARATIVE COMMAND REGISTRY
// ═══════════════════════════════════════════════════════════════════════════════

/** Context passed to every command execute function */
interface CommandContext {
  senderId: string
  channelId: string
  session: SessionState
  ctx: any
  event: any
}

/**
 * A single registered command.
 * - pattern: regex to match against trimmed user message
 * - mode: 'read' = routeCommandDirect only, 'write' = routeCommand only, 'both' = both paths
 * - execute: returns reply text (string), or null if not actually handled (conditional commands)
 *            May be async for commands that do dynamic imports.
 */
interface SoulCommand {
  pattern: RegExp
  mode: 'read' | 'write' | 'both'
  execute: (match: RegExpMatchArray, c: CommandContext) => string | null | Promise<string | null>
}

// ── Help texts (different for routeCommand vs routeCommandDirect) ──
const HELP_TEXT_FULL = `cc-soul 命令指南

━━ 自动运行（无需操作） ━━
• 记忆：每条对话自动记录、去重、衰减、矛盾检测
• 人格：11种人格根据对话内容自动切换（工程师/朋友/严师/分析师/安抚者/军师/探索者/执行者/导师/魔鬼代言人/苏格拉底）
• 情绪：实时追踪你的情绪，自动调整回应风格
• 学习：从你的纠正中学习规则，3次验证后永久生效
• 举一反三：回答问题时自动补充你可能需要的相关信息

━━ 触发词（说出即生效） ━━
• "帮我理解" / "引导我" / "别告诉我答案" → 苏格拉底模式（用提问引导你）
• "隐私模式" / "别记了" → 暂停记忆 | "可以了" → 恢复
• "上次聊..." / "接着聊..." → 自动回忆相关话题

━━ 记忆管理 ━━
• 我的记忆 / my memories          — 查看最近记忆
• 搜索记忆 <关键词>               — 搜索记忆
• 删除记忆 <关键词>               — 删除匹配记忆
• pin 记忆 <关键词>               — 钉选（永不衰减）
• unpin 记忆 <关键词>             — 取消钉选
• 记忆时间线 <关键词>             — 查看变化历史
• 记忆健康                        — 记忆统计报告
• 记忆审计                        — 检查重复/异常
• 恢复记忆 <关键词>               — 恢复归档记忆

━━ 导入导出 ━━
• 导出全部 / export all / full backup — 全量备份（已去敏）
• 导入全部 <路径> / import all <path> — 从全量备份恢复
• 导出lorebook                    — 导出知识库（去敏）
• 导出进化 / export evolution      — 导出 GEP 格式进化资产
• 导入进化 <路径>                  — 导入 GEP 格式进化资产
• 摄入文档 <路径> / ingest <path> — 导入文档到记忆

━━ 状态查看 ━━
• stats                           — 个人仪表盘
• soul state                      — AI 能量/心情/情绪
• 情绪周报 / mood report          — 7天情绪趋势
• 能力评分 / capability score     — 各领域能力评分
• 我的技能 / my skills            — 自动生成的技能列表
• metrics / 监控                  — 系统运行指标
• cost / 成本                     — Token 使用统计
• dashboard / 仪表盘              — 打开网页仪表盘
• 记忆图谱 html                   — 打开记忆可视化
• 对话摘要                        — 最近对话摘要

━━ 记忆洞察 ━━
• 时间旅行 <关键词>               — 追踪某个话题的观点演变
• 推理链 / reasoning chain        — 查看上次回复用了哪些记忆
• 情绪锚点 / emotion anchors      — 查看话题与情绪的关联
• 记忆链路 <关键词>               — 搜索相关记忆并展示关联链

━━ 体验功能 ━━
• 保存话题 / save topic           — 保存当前对话上下文为话题分支
• 切换话题 <名称> / switch topic  — 恢复保存的话题分支
• 话题列表 / topic list           — 查看所有话题分支
• 共享记忆 <关键词>               — 将匹配记忆设为全局共享
• 私有记忆 <关键词>               — 将匹配记忆设为私有

━━ 高级功能 ━━
• 功能状态 / features             — 查看所有功能开关
• 开启 <功能> / 关闭 <功能>       — 开关功能
• 开始实验 <描述>                 — 启动 A/B 实验

向量搜索已退役，NAM 记忆引擎已覆盖语义匹配。`

const HELP_TEXT_DIRECT = `cc-soul 命令指南

━━ 自动运行（无需操作） ━━
• 记忆/人格/情绪/学习/举一反三 全自动

━━ 命令 ━━
帮助 — 显示此指南
搜索记忆 <关键词> — 搜索记忆
我的记忆 — 查看最近记忆
stats — 个人仪表盘
soul state — AI 能量/心情
情绪周报 — 7天情绪趋势
能力评分 — 各领域评分
功能状态 — 功能开关
记忆健康 — 记忆统计
导出全部 / export all — 全量备份
导入全部 <路径> / import all — 全量恢复
导出进化 — 导出 GEP 格式进化资产
导入进化 <路径> — 导入 GEP 格式

━━ 触发词 ━━
"别记了" → 暂停记忆 | "可以了" → 恢复
"帮我理解" → 苏格拉底模式`

/**
 * Command registry — order matches original if/else chain in routeCommand.
 * Commands with mode 'both' or 'read' are also available in routeCommandDirect.
 *
 * IMPORTANT: Do NOT reorder — first match wins, just like the original if/else.
 */
const COMMANDS: SoulCommand[] = [
  // ── Help ──
  {
    pattern: /^(help|帮助|命令列表|commands)$/i,
    mode: 'both',
    execute: () => HELP_TEXT_FULL,  // routeCommandDirect overrides with HELP_TEXT_DIRECT
  },

  // ── Privacy mode ON ──
  {
    pattern: /^(别记了|隐私模式|privacy mode)$/i,
    mode: 'both',
    execute: () => {
      setPrivacyMode(true)
      console.log('[cc-soul] privacy mode ON')
      return '隐私模式已开启，对话内容不会被记忆。说"可以了"恢复。'
    },
  },

  // ── Privacy mode OFF ──
  {
    pattern: /^(可以了|关闭隐私|恢复记忆)$/i,
    mode: 'both',
    execute: () => {
      if (!getPrivacyMode()) return null  // not in privacy mode, skip
      setPrivacyMode(false)
      console.log('[cc-soul] privacy mode OFF')
      return '隐私模式已关闭，恢复记忆。'
    },
  },

  // ── Document ingest ──
  {
    pattern: /^(摄入文档|ingest)\s+(.+)$/i,
    mode: 'write',
    execute: (m, c) => {
      const filePath = m[2].trim()
      const resolvedPath = resolve(filePath.replace(/^~/, homedir()))
      const safeRoots = [homedir(), '/tmp']
      if (!safeRoots.some(root => resolvedPath.startsWith(root))) {
        return '安全限制：只能导入家目录或 /tmp 下的文件。'
      }
      const count = ingestFile(filePath, c.senderId, c.channelId)
      if (count >= 0) {
        return `已摄入 ${count} 个片段，来源: "${filePath}"`
      } else {
        return `文件读取失败: "${filePath}"，请检查路径和权限。`
      }
    },
  },

  // ── Metrics / 监控 ──
  {
    pattern: /^(metrics|监控|运行状态)$/i,
    mode: 'write',
    execute: () => formatMetrics(),
  },

  // ── Dashboard ──
  {
    pattern: /^(dashboard|仪表盘)$/i,
    mode: 'write',
    execute: () => {
      const htmlPath = generateDashboardHTML()
      exec(`open "${htmlPath}"`)
      return `Dashboard generated and opened: ${htmlPath}`
    },
  },

  // ── 记忆图谱 HTML ──
  {
    pattern: /^(记忆图谱\s*html|memory map\s*html)$/i,
    mode: 'write',
    execute: () => {
      const htmlPath = generateMemoryMapHTML()
      exec(`open "${htmlPath}"`)
      return `已生成记忆图谱 HTML 并打开: ${htmlPath}`
    },
  },

  // ── 情绪周报 ──
  {
    pattern: /^(情绪周报|mood report)$/i,
    mode: 'both',
    execute: () => {
      try {
        const report = generateMoodReport()
        return report || '暂无足够数据生成情绪周报。'
      } catch (_) { return '情绪周报暂不可用' }
    },
  },

  // ── 能力评分 ──
  {
    pattern: /^(能力评分|capability score|capability)$/i,
    mode: 'both',
    execute: () => {
      try {
        const score = getCapabilityScore()
        return typeof score === 'string' ? score : JSON.stringify(score, null, 2)
      } catch (_) { return '能力评分暂不可用' }
    },
  },

  // ── Cost / Token usage ──
  {
    pattern: /^(cost|token cost|token使用|成本)$/i,
    mode: 'both',
    execute: () => getCostSummary(),
  },

  // ── 开始实验 ──
  {
    pattern: /^开始实验(.*)$/i,
    mode: 'write',
    execute: () => '实验功能已退役。参数调优已由 auto-tune 自动处理。',
  },

  // ── 向量搜索退役提示 ──
  {
    pattern: /^(安装向量|install vector|向量状态|vector status)$/i,
    mode: 'write',
    execute: () => '向量搜索已退役，NAM 记忆引擎已覆盖语义匹配，无需额外安装。',
  },

  // ── 我的技能 ──
  {
    pattern: /^(我的技能|my skills)$/i,
    mode: 'write',
    execute: () => {
      try {
        const skillsPath = resolve(DATA_DIR, 'skills.json')
        const skills = loadJson(skillsPath, [])
        if (skills.length === 0) return '还没有发现技能。多聊几轮后会自动生成。'
        const list = skills.slice(0, 10).map((s: any, i: number) => `${i + 1}. ${s.name || s.pattern || s.content?.slice(0, 40) || '未命名'}`).join('\n')
        return `你的技能（${skills.length} 个）：\n${list}`
      } catch { return '技能列表暂不可用。' }
    },
  },

  // ── 灵魂模式 ON ──
  {
    pattern: /^[\/]?灵魂模式\s*(.*)$/i,
    mode: 'write',
    execute: (m) => {
      const speaker = m[1]?.trim() || ''
      setSoulMode(true, speaker)
      return speaker
        ? `灵魂模式已开启（身份：${speaker}）。发 /退出灵魂 可关闭。`
        : `灵魂模式已开启，会自动识别对方身份。发 /退出灵魂 可关闭，发 /我是 <名字> 可指定身份。`
    },
  },

  // ── 灵魂模式 OFF ──
  {
    pattern: /^[\/]?(退出灵魂|关闭灵魂|灵魂模式关|soul.mode.off)$/i,
    mode: 'write',
    execute: () => {
      setSoulMode(false)
      return `灵魂模式已关闭，恢复正常对话。`
    },
  },

  // ── 灵魂模式切换身份 ──
  {
    pattern: /^[\/]?我是\s+(.+)$/i,
    mode: 'write',
    execute: (m) => {
      if (!getSoulMode().active) return null  // not in soul mode, skip
      const newSpeaker = m[1].trim()
      setSoulMode(true, newSpeaker)
      return `好的，现在你是「${newSpeaker}」。`
    },
  },

  // ── 我的记忆 ──
  {
    pattern: /^(我的记忆|my memories)$/i,
    mode: 'both',
    execute: (_m, c) => executeMyMemories(c.senderId),
  },

  // ── 搜索记忆 ──
  {
    pattern: /^(搜索记忆|search memory)\s+(.+)$/i,
    mode: 'both',
    execute: (m, c) => executeSearch(m[2].trim(), c.senderId),
  },

  // ── 删除记忆 ──
  {
    pattern: /^(删除记忆|delete memory)\s+(.+)$/i,
    mode: 'write',
    execute: (m, c) => {
      const keyword = m[2].trim()
      const results = recall(keyword, 10, c.senderId)
      if (results.length === 0) return `没有找到匹配「${keyword}」的记忆可删除。`
      ensureMemoriesLoaded()
      let expired = 0
      for (const r of results) {
        const idx = memoryState.memories.findIndex(m => m.ts === r.ts && m.content === r.content)
        if (idx >= 0) { memoryState.memories[idx].scope = 'expired'; expired++ }
      }
      if (expired > 0) saveMemories()
      return `已标记 ${expired} 条匹配 "${keyword}" 的记忆为过期。`
    },
  },

  // ── 导出 lorebook ──
  {
    pattern: /^(导出lorebook|export lorebook)$/i,
    mode: 'write',
    execute: () => {
      const exportDir = DATA_DIR + '/export'
      if (!existsSync(exportDir)) mkdirSync(exportDir, { recursive: true })
      const lorebookPath = resolve(DATA_DIR, 'lorebook.json')
      let raw: any[] = []
      try { raw = loadJson(lorebookPath, []) } catch { /* corrupted lorebook.json */ }
      const sanitized = raw
        .filter((e: any) => e.enabled !== false)
        .map((e: any) => ({
          keywords: e.keywords || [],
          content: (e.content || '').replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '[REDACTED]')
            .replace(/\b(?:sk-|api[_-]?key|token|secret|password)[=:]\s*\S+/gi, '[REDACTED]'),
          category: e.category || 'fact',
          priority: e.priority || 5,
        }))
      const exportPath = `${exportDir}/lorebook_share.json`
      writeFileSync(exportPath, JSON.stringify({ knowledge: sanitized, version: 1, exportedAt: new Date().toISOString() }, null, 2), 'utf-8')
      return `已导出 ${sanitized.length} 条 lorebook 到 ${exportPath}（已去敏，兼容 ClawHub knowledge 格式）`
    },
  },

  // ── 导出进化 ──
  {
    pattern: /^(导出进化|export evolution)$/i,
    mode: 'both',
    execute: async () => {
      try {
        if (!_exportEvolutionAssets) {
          // Try dynamic import for routeCommandDirect path
          try {
            const mod = await import('./evolution.ts')
            _exportEvolutionAssets = mod.exportEvolutionAssets
          } catch (_) {}
        }
        if (!_exportEvolutionAssets) return '进化模块未加载'
        const { data, path } = _exportEvolutionAssets({ totalMessages: stats.totalMessages, firstSeen: stats.firstSeen, corrections: stats.corrections })
        return `进化资产已导出 (GEP v${data.version})\n` +
          `  规则: ${data.assets.rules.length}\n` +
          `  假设: ${data.assets.hypotheses.length}\n` +
          `  技能: ${data.assets.skills?.length ?? 0}\n` +
          `  已固化: ${data.assets.metadata.rulesSolidified}\n` +
          `路径: ${path}`
      } catch (e: any) { return `导出进化失败: ${e.message}` }
    },
  },

  // ── 导入进化 ──
  {
    pattern: /^(导入进化|import evolution)\s+(.+)$/i,
    mode: 'both',
    execute: async (m) => {
      const filePath = m[2].trim().replace(/^~/, homedir())
      try {
        if (!existsSync(filePath)) return `文件不存在: ${filePath}`
        if (!filePath.startsWith(homedir()) && !filePath.startsWith('/tmp')) return '安全限制：只能导入家目录或 /tmp 下的文件。'
        if (!_importEvolutionAssets) {
          try {
            const mod = await import('./evolution.ts')
            _importEvolutionAssets = mod.importEvolutionAssets
          } catch (_) {}
        }
        if (!_importEvolutionAssets) return '进化模块未加载'
        const { rulesAdded, hypothesesAdded } = _importEvolutionAssets(filePath)
        return `进化资产已导入 (GEP)\n  新增规则: ${rulesAdded}\n  新增假设: ${hypothesesAdded}`
      } catch (e: any) { return `导入进化失败: ${e.message}` }
    },
  },

  // ── 导出全部 ──
  {
    pattern: /^(导出全部|export all|full backup)$/i,
    mode: 'both',
    execute: () => {
      try {
        const { path, counts } = _fullBackup()
        const lines = Object.entries(counts).map(([k, v]) => `  ${k}: ${v}`)
        return `全量备份已导出（已去敏）\n${lines.join('\n')}\n路径: ${path}`
      } catch (e: any) { return `全量备份失败: ${e.message}` }
    },
  },

  // ── 导入全部 ──
  {
    pattern: /^(导入全部|import all)\s+(.+)$/i,
    mode: 'both',
    execute: (m) => {
      const fp = m[2].trim().replace(/^~/, homedir())
      try {
        if (!existsSync(fp)) return `文件不存在: ${fp}`
        if (!fp.startsWith(homedir()) && !fp.startsWith('/tmp')) return '安全限制：只能导入家目录或 /tmp 下的文件。'
        const counts = _fullRestore(fp)
        const lines = Object.entries(counts).map(([k, v]) => `  ${k}: ${v}`)
        return `全量恢复完成（需重启生效）\n${lines.join('\n')}`
      } catch (e: any) { return `全量恢复失败: ${e.message}` }
    },
  },

  // ── 记忆链路 ──
  {
    pattern: /^(记忆链路|memory chain)\s+(.+)$/i,
    mode: 'both',
    execute: (m) => {
      try { return generateMemoryChain(m[2].trim()) } catch (e: any) { return '记忆链路生成失败: ' + e.message }
    },
  },

  // ── 保存话题 ──
  {
    pattern: /^(保存话题|save topic)$/i,
    mode: 'write',
    execute: () => {
      try {
        const branchDir = resolve(DATA_DIR, 'branches')
        if (!existsSync(branchDir)) mkdirSync(branchDir, { recursive: true })
        const recentMsgs = memoryState.chatHistory.slice(-10)
        const topicWords = recentMsgs.flatMap(h => (h.user || '').match(/[\u4e00-\u9fff]{2,4}|[A-Za-z]{3,}/g) || [])
        const freq = new Map<string, number>()
        for (const w of topicWords) { const k = w.toLowerCase(); freq.set(k, (freq.get(k) || 0) + 1) }
        const topicLabel = [...freq.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || `topic_${Date.now()}`
        const branchData = {
          topic: topicLabel,
          savedAt: Date.now(),
          chatHistory: recentMsgs,
          persona: getActivePersona().id,
        }
        const branchPath = resolve(branchDir, `${topicLabel}.json`)
        writeFileSync(branchPath, JSON.stringify(branchData, null, 2), 'utf-8')
        return `话题已保存：「${topicLabel}」（${recentMsgs.length} 轮对话）\n路径: ${branchPath}`
      } catch (e: any) { return '保存话题失败: ' + e.message }
    },
  },

  // ── 切换话题 ──
  {
    pattern: /^(切换话题|switch topic)\s+(.+)$/i,
    mode: 'write',
    execute: (m) => {
      try {
        const topicName = m[2].trim()
        const branchDir = resolve(DATA_DIR, 'branches')
        const branchPath = resolve(branchDir, `${topicName}.json`)
        if (!branchPath.startsWith(branchDir)) return '无效的话题名称。'
        // Save current conversation before switching
        if (memoryState.chatHistory.length > 0) {
          if (!existsSync(branchDir)) mkdirSync(branchDir, { recursive: true })
          const currentTopic = `_autosave_${Date.now()}`
          const currentBranch = { topic: currentTopic, savedAt: Date.now(), chatHistory: memoryState.chatHistory.slice(-50) }
          saveJson(resolve(branchDir, `${currentTopic}.json`), currentBranch)
        }
        if (!existsSync(branchPath)) return `话题「${topicName}」不存在，用"话题列表"查看可用话题。`
        const branchData = loadJson(branchPath, {} as any)
        if (branchData.chatHistory && Array.isArray(branchData.chatHistory)) {
          memoryState.chatHistory.length = 0
          memoryState.chatHistory.push(...branchData.chatHistory)
        }
        const persona = branchData.persona || 'unknown'
        return `已切换到话题「${topicName}」（恢复 ${branchData.chatHistory?.length || 0} 轮对话，人格: ${persona}）`
      } catch (e: any) { return '切换话题失败: ' + e.message }
    },
  },

  // ── 话题列表 ──
  {
    pattern: /^(话题列表|topic list)$/i,
    mode: 'both',
    execute: () => {
      try {
        const branchDir = resolve(DATA_DIR, 'branches')
        if (!existsSync(branchDir)) return '暂无保存的话题。'
        const files = (readdirSync(branchDir) as string[]).filter((f: string) => f.endsWith('.json'))
        if (files.length === 0) return '暂无保存的话题。'
        const lines: string[] = [`话题列表（${files.length} 个）：`]
        for (const f of files) {
          try {
            const data = loadJson(resolve(branchDir, f), {} as any)
            const age = Math.floor((Date.now() - (data.savedAt || 0)) / 86400000)
            const ageStr = age === 0 ? '今天' : `${age}天前`
            lines.push(`• ${data.topic || f.replace('.json', '')} — ${data.chatHistory?.length || 0} 轮对话（${ageStr}）`)
          } catch { lines.push(`• ${f.replace('.json', '')} — 数据损坏`) }
        }
        return lines.join('\n')
      } catch (e: any) { return '话题列表读取失败: ' + e.message }
    },
  },

  // ── 共享记忆 ──
  {
    pattern: /^(共享记忆|share memory)\s+(.+)$/i,
    mode: 'write',
    execute: (m) => {
      try {
        const keyword = m[2].trim()
        const _db = getDb()
        if (!_db) return '数据库未就绪。'
        const kw = `%${keyword.toLowerCase()}%`
        const stmt = _db.prepare("UPDATE memories SET visibility = 'global' WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?)")
        const result = stmt.run(kw, kw)
        const changed = result.changes || 0
        return changed > 0
          ? `已将 ${changed} 条匹配「${keyword}」的记忆设为全局共享。`
          : `没有找到匹配「${keyword}」的记忆。`
      } catch (e: any) { return '共享记忆失败: ' + e.message }
    },
  },

  // ── 私有记忆 ──
  {
    pattern: /^(私有记忆|private memory)\s+(.+)$/i,
    mode: 'write',
    execute: (m) => {
      try {
        const keyword = m[2].trim()
        const _db = getDb()
        if (!_db) return '数据库未就绪。'
        const kw = `%${keyword.toLowerCase()}%`
        const stmt = _db.prepare("UPDATE memories SET visibility = 'private' WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?)")
        const result = stmt.run(kw, kw)
        const changed = result.changes || 0
        return changed > 0
          ? `已将 ${changed} 条匹配「${keyword}」的记忆设为私有。`
          : `没有找到匹配「${keyword}」的记忆。`
      } catch (e: any) { return '私有记忆失败: ' + e.message }
    },
  },

  // ── 对话摘要 ──
  {
    pattern: /^(对话摘要|conversation summary)$/i,
    mode: 'write',
    execute: () => {
      let allHistory = memoryState.chatHistory
      if (allHistory.length === 0) {
        try {
          const histPath = resolve(DATA_DIR, 'history.json')
          allHistory = loadJson(histPath, [])
        } catch (_) {}
      }
      const recent = allHistory.slice(-25)
      const sessions: { start: number; turns: typeof recent; summary: string }[] = []
      let cur: typeof recent = []
      for (const turn of recent) {
        if (cur.length > 0 && turn.ts - cur[cur.length - 1].ts > 1800000) {
          sessions.push({ start: cur[0].ts, turns: cur, summary: '' })
          cur = []
        }
        cur.push(turn)
      }
      if (cur.length > 0) sessions.push({ start: cur[0].ts, turns: cur, summary: '' })

      const lines = sessions.slice(-5).map((s, i) => {
        const date = new Date(s.start).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
        const topics = s.turns.slice(0, 3).map(t => t.user.slice(0, 30)).join(' → ')
        return `${i + 1}. [${date}] ${s.turns.length} 轮 | ${topics}...`
      })
      return `最近对话摘要（${sessions.length} 个会话）：\n${lines.join('\n') || '暂无记录'}`
    },
  },

  // ── 记忆健康 ──
  {
    pattern: /^(记忆健康|memory health)$/i,
    mode: 'both',
    execute: () => executeHealth(),
  },

  // ── 记忆审计 ──
  {
    pattern: /^(记忆审计|memory audit)$/i,
    mode: 'write',
    execute: () => {
      const auditPath = resolve(DATA_DIR, 'memory_audit.json')
      const audit = loadJson<any>(auditPath, null)
      if (!audit) return '暂无审计报告，等待下次心跳自动生成'
      const lines = [
        `记忆审计报告（${new Date(audit.ts).toLocaleString()}）`,
        `重复记忆: ${audit.duplicates?.length ?? 0} 组`,
        `极短记忆(<10字): ${audit.tooShort?.length ?? 0} 条`,
        `无标签活跃记忆: ${audit.untagged ?? 0} 条`,
        audit.suggestions ? `建议: ${audit.suggestions}` : '',
      ].filter(Boolean)
      return `记忆审计结果：\n${lines.join('\n')}`
    },
  },

  // ── Pin / Unpin 记忆 ──
  {
    pattern: /^(pin|unpin)\s*(记忆|memory)\s+(.+)$/i,
    mode: 'write',
    execute: (m, c) => {
      const action = m[1].toLowerCase() as 'pin' | 'unpin'
      const keyword = m[3].trim()
      const results = recall(keyword, 10, c.senderId)
      if (results.length === 0) return `没有找到匹配 "${keyword}" 的记忆。`
      ensureMemoriesLoaded()
      let changed = 0
      const newScope = action === 'pin' ? 'pinned' : 'mid_term'
      for (const r of results) {
        const mem = memoryState.memories.find(m => m.content === r.content && m.ts === r.ts)
        if (mem && mem.scope !== newScope) { mem.scope = newScope; changed++ }
      }
      if (changed > 0) saveMemories()
      return action === 'pin'
        ? `已钉选 ${changed} 条匹配 "${keyword}" 的记忆（不会被衰减淘汰）`
        : `已取消钉选 ${changed} 条匹配 "${keyword}" 的记忆（恢复为 mid_term）`
    },
  },

  // ── 恢复记忆 ──
  {
    pattern: /^(?:恢复记忆|restore memory)\s+(.+)$/i,
    mode: 'write',
    execute: (m) => {
      try {
        const keyword = m[1].trim()
        const count = restoreArchivedMemories(keyword)
        return count > 0
          ? `已恢复 ${count} 条匹配 "${keyword}" 的归档记忆。`
          : `没有找到匹配 "${keyword}" 的归档记忆。`
      } catch (e: any) { return `恢复失败: ${e.message}` }
    },
  },

  // ── 记忆时间线 ──
  {
    pattern: /^(记忆时间线|时间线|memory timeline)\s+(.+)$/i,
    mode: 'write',
    execute: (m) => {
      const keyword = m[2].trim()
      const results = queryMemoryTimeline(keyword)
      if (results.length === 0) return `没有找到关键词 "${keyword}" 的记忆时间线。`
      const lines = results.map(r => {
        const from = new Date(r.from).toLocaleString()
        const until = r.until ? new Date(r.until).toLocaleString() : '至今'
        return `- [${from} ~ ${until}] ${r.content.slice(0, 80)}`
      })
      return `记忆时间线 "${keyword}"（${results.length} 条）：\n${lines.join('\n')}`
    },
  },

  // ── 时间旅行 ──
  {
    pattern: /^(?:时间旅行|time travel)\s+(.+)$/i,
    mode: 'write',
    execute: (m) => {
      const keyword = m[1].trim()
      try {
        const _db = getDb()
        if (!_db) return '数据库未就绪，无法查询。'
        const kw = `%${keyword.toLowerCase()}%`
        const rows = _db.prepare(
          "SELECT content, scope, ts FROM memories WHERE LOWER(content) LIKE ? AND scope != 'expired' AND scope != 'decayed' ORDER BY ts ASC LIMIT 30"
        ).all(kw) as any[]
        if (rows.length === 0) return `没有找到关于「${keyword}」的记忆演变。`
        const lines = rows.map((r: any) => {
          const date = new Date(r.ts).toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
          return `  [${date}] ${r.content.slice(0, 80)}`
        })
        let trend = '→ 持续关注中'
        if (rows.length >= 3) {
          const first = rows[0].content.toLowerCase()
          const last = rows[rows.length - 1].content.toLowerCase()
          if (first.includes('学') && last.includes('理解')) trend = '→ 从入门到深入，持续推进中'
          else if (last.includes('完成') || last.includes('done')) trend = '→ 已完成'
          else if (last.includes('放弃') || last.includes('算了')) trend = '→ 已放弃'
        }
        return `🕰 「${keyword}」观点演变（${rows.length} 条）\n${lines.join('\n')}\n\n${trend}`
      } catch (e: any) { return `时间旅行查询失败: ${e.message}` }
    },
  },

  // ── 推理链 ──
  {
    pattern: /^(推理链|reasoning chain)$/i,
    mode: 'write',
    execute: (_m, c) => {
      const recalled = c.session.lastRecalledContents
      if (recalled.length === 0) return '上一次回复没有召回任何记忆。'
      const lines = recalled.map((ct, i) => `  ${i + 1}. ${ct.slice(0, 100)}`)
      // ── 因果追溯 ──
      const causalLines: string[] = []
      const DAY_MS = 24 * 3600000
      const allMems = memoryState.memories
      const recalledMems = recalled.map(ct => allMems.find(m => m.content === ct)).filter(Boolean) as typeof allMems
      const correctionMems = recalledMems.filter(m => m.scope === 'correction' || m.scope === 'event')
      for (const mem of correctionMems.slice(0, 3)) {
        const memTrigrams = trigrams(mem.content)
        const nearby = allMems.filter(m =>
          m !== mem && Math.abs(m.ts - mem.ts) < DAY_MS &&
          trigramSimilarity(trigrams(m.content), memTrigrams) > 0.15
        ).sort((a, b) => a.ts - b.ts)
        if (nearby.length > 0) {
          const rootCause = nearby[0]
          const fmtD = (ts: number) => new Date(ts).toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
          causalLines.push(`  结果: ${mem.content.slice(0, 60)} (${fmtD(mem.ts)})`)
          causalLines.push(`    ← 原因: ${nearby[nearby.length > 1 ? 1 : 0].content.slice(0, 60)} (${fmtD(nearby[0].ts)})`)
          causalLines.push(`    ← 根因: ${rootCause.content.slice(0, 60)}`)
          const rootSnippet = rootCause.content.slice(0, 40).replace(/[。.!！？?]$/, '')
          causalLines.push(`  💭 反事实: 如果当时没有「${rootSnippet}」，这个问题可能不会发生`)
          causalLines.push('')
        }
      }
      let display = `🧠 上次回复的推理链（召回 ${recalled.length} 条记忆）：\n${lines.join('\n')}`
      if (causalLines.length > 0) {
        display += `\n\n🔗 因果追溯：\n${causalLines.join('\n')}`
      }
      return display
    },
  },

  // ── 情绪锚点 ──
  {
    pattern: /^(情绪锚点|emotion anchors?)$/i,
    mode: 'write',
    execute: () => formatEmotionAnchors(),
  },

  // ── "别记这个" — skip next memory ──
  {
    pattern: /^(别记了?这[个条]?|别记住|don't remember|forget this|不要记)/i,
    mode: 'write',
    execute: (_m, c) => {
      c.session._skipNextMemory = true
      return '🔇 收到，这条对话不会被记忆。'
    },
  },

  // ── stats (write path) ──
  {
    pattern: /^(stats)$/i,
    mode: 'both',
    execute: () => executeStats(),
  },

  // ── 功能状态 ──
  {
    pattern: /^(功能状态|features|feature status)$/i,
    mode: 'both',
    execute: () => executeFeatures(),
  },

  // ── 功能开关 toggle ──
  {
    pattern: /^(?:开启|启用|enable|关闭|禁用|disable)\s+\S+$/i,
    mode: 'both',
    execute: (m) => {
      const result = handleFeatureCommand(m[0])
      if (result) return typeof result === 'string' ? result : '功能开关已更新。'
      return null  // not handled
    },
  },

  // ── 灵魂状态 ──
  {
    pattern: /^(soul state|灵魂状态|内心状态)$/i,
    mode: 'read',
    execute: async () => {
      try {
        const { body } = await import('./body.ts')
        return `灵魂状态\nEnergy: ${(body.energy * 100).toFixed(0)}%\nMood: ${body.mood.toFixed(2)}\nEmotion: ${body.emotion}`
      } catch (_) { return '灵魂状态暂不可用' }
    },
  },

  // ── 人格列表 ──
  {
    pattern: /^(人格列表|personas?)$/i,
    mode: 'read',
    execute: async () => {
      try {
        const { PERSONAS } = await import('./persona.ts')
        const lines = PERSONAS.map((p: any) => `• ${p.name} — ${p.tone?.slice(0, 40) || ''}`)
        return `人格列表：\n${lines.join('\n')}`
      } catch (_) { return '人格列表不可用' }
    },
  },

  // ── 价值观 ──
  {
    pattern: /^(价值观|values)$/i,
    mode: 'read',
    execute: () => {
      try {
        const vals = getAllValues()
        return typeof vals === 'string' ? vals : JSON.stringify(vals, null, 2).slice(0, 500)
      } catch (_) { return '价值观模块不可用' }
    },
  },

  // LLM 配置命令已移除 — 通过 system prompt 注入指引，让 OpenClaw 的 LLM 自然引导用户编辑 ai_config.json
]

// ═══════════════════════════════════════════════════════════════════════════════
// COMMAND MATCHER
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Match a message against the command registry.
 * @param msg - trimmed user message
 * @param allowWrite - if false, skip commands with mode='write'
 * @returns matched command + regex match, or null
 */
function matchCommand(msg: string, allowWrite: boolean): { cmd: SoulCommand; match: RegExpMatchArray } | null {
  for (const cmd of COMMANDS) {
    if (!allowWrite && cmd.mode === 'write') continue
    const m = msg.trim().match(cmd.pattern)
    if (m) return { cmd, match: m }
  }
  return null
}

// ═══════════════════════════════════════════════════════════════════════════════
// routeCommand — full command handler (write + read)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Route user commands. Returns true if the command was handled (caller should return early).
 */
export function routeCommand(
  userMsg: string,
  ctx: any,
  session: SessionState,
  senderId: string,
  channelId: string,
  event: any,
): boolean {
  console.log(`[cc-soul][routeCommand] v2 msg="${userMsg.slice(0,30)}"`)

  // ── Dedup: skip if already handled by routeCommandDirect (inbound_claim path) ──
  if (wasHandledByDirect(userMsg)) {
    console.log(`[cc-soul][routeCommand] skipped: already handled by routeCommandDirect`)
    ctx.bodyForAgent = '[系统] 命令已处理，结果已发送。'
    return true
  }

  // ── Visual memory: detect image/screenshot descriptions injected by OpenClaw vision ──
  if (!getPrivacyMode()) {
    const imageMatch = userMsg.match(/\[(?:Image|图片|Screenshot|截图)[:\s]([^\]]+)\]/i)
    if (imageMatch) {
      addMemory(`[视觉记忆] ${imageMatch[1].slice(0, 200)}`, 'visual', senderId, 'channel', channelId)
      console.log(`[cc-soul][visual] stored image memory: ${imageMatch[1].slice(0, 60)}`)
    }
  }

  // ── Feature toggle (non-regex — uses external handleFeatureCommand) ──
  const featureResult = handleFeatureCommand(userMsg)
  if (featureResult) {
    cmdReply(ctx, event, session, typeof featureResult === 'string' ? featureResult : '功能开关已更新。', userMsg)
    return true
  }

  // ── Quick shortcuts (Feature 3) ──
  const shortcutCmd = shortcuts[userMsg.trim()]
  if (shortcutCmd) {
    if (shortcutCmd === '功能状态') {
      const result = handleFeatureCommand('功能状态')
      cmdReply(ctx, event, session, typeof result === 'string' ? result : '功能开关已更新。', userMsg)
      return true
    }
    if (shortcutCmd === '记忆图谱') {
      cmdReply(ctx, event, session, '记忆图谱功能已触发，请稍候。', userMsg)
      return true
    }
    if (shortcutCmd === '最近在聊什么') {
      const recentTopics = memoryState.chatHistory.slice(-5).map(h => h.user.slice(0, 30)).join(' → ')
      cmdReply(ctx, event, session, `最近话题轨迹: ${recentTopics || '暂无记录'}`, userMsg)
      return true
    }
    if (shortcutCmd === '紧急模式') {
      cmdReply(ctx, event, session, '紧急模式已开启，将提供快速精准的回答。', userMsg)
      return true
    }
  }

  // User dashboard retired — handleDashboardCommand removed

  // ── Auto-tune commands (non-regex — uses external handleTuneCommand) ──
  if (handleTuneCommand(userMsg)) {
    cmdReply(ctx, event, session, '调参指令已执行。', userMsg)
    return true
  }

  // ── Registry-based command matching ──
  const matched = matchCommand(userMsg, true)
  if (matched) {
    const cmdCtx: CommandContext = { senderId, channelId, session, ctx, event }
    const result = matched.cmd.execute(matched.match, cmdCtx)
    if (result instanceof Promise) {
      // Async command — fire and forget with reply
      result.then(text => {
        if (text != null) cmdReply(ctx, event, session, text, userMsg)
      }).catch((e: any) => {
        cmdReply(ctx, event, session, `命令执行失败: ${e.message}`, userMsg)
      })
      // Mark as handled immediately (reply will arrive async)
      ctx.bodyForAgent = '[系统] 命令已处理，结果已发送。'
      return true
    }
    if (result != null) {
      cmdReply(ctx, event, session, result, userMsg)
      return true
    }
    // result === null means conditional command didn't match (e.g. privacy OFF when not in privacy mode)
  }

  // ── #11 上下文提醒命令 (multi-pattern, kept inline) ──
  {
    const ctxMatch1 = userMsg.match(/^当聊到\s*(.+?)\s*时?提醒我\s+(.+)$/)
    const ctxMatch2 = userMsg.match(/^remind\s+me\s+(.+?)\s+when\s+(?:we\s+)?talk(?:ing)?\s+about\s+(.+)$/i)
    const ctxMatch3 = userMsg.match(/^when\s+(?:we\s+)?talk(?:ing)?\s+about\s+(.+?)\s+remind\s+me\s+(.+)$/i)
    if (ctxMatch1) {
      const keyword = ctxMatch1[1].trim()
      const reminderContent = ctxMatch1[2].trim()
      if (keyword.length >= 2 && reminderContent.length >= 2) {
        const id = dbAddContextReminder(keyword, reminderContent, senderId)
        cmdReply(ctx, event, session, `已添加上下文提醒：当聊到「${keyword}」时提醒你「${reminderContent}」(id=${id})`, userMsg)
        return true
      }
    } else if (ctxMatch2) {
      const reminderContent = ctxMatch2[1].trim()
      const keyword = ctxMatch2[2].trim()
      if (keyword.length >= 2 && reminderContent.length >= 2) {
        const id = dbAddContextReminder(keyword, reminderContent, senderId)
        cmdReply(ctx, event, session, `已添加上下文提醒：当聊到「${keyword}」时提醒你「${reminderContent}」(id=${id})`, userMsg)
        return true
      }
    } else if (ctxMatch3) {
      const keyword = ctxMatch3[1].trim()
      const reminderContent = ctxMatch3[2].trim()
      if (keyword.length >= 2 && reminderContent.length >= 2) {
        const id = dbAddContextReminder(keyword, reminderContent, senderId)
        cmdReply(ctx, event, session, `已添加上下文提醒：当聊到「${keyword}」时提醒你「${reminderContent}」(id=${id})`, userMsg)
        return true
      }
    }
  }

  // ── Task confirmation check (non-regex — uses external checkTaskConfirmation) ──
  const chatId = (ctx.conversationId || event.sessionKey || '') as string
  if (checkTaskConfirmation(userMsg, chatId)) {
    cmdReply(ctx, event, session, '任务已派发给执行引擎，正在处理中...', userMsg)
    return true
  }

  // Fallback: try routeCommandDirect for commands only handled there (人格列表, 审计, 价值观 etc.)
  if (isCommand(userMsg)) {
    const evCtx = event?.context || {}
    const to = evCtx.conversationId || evCtx.chatId || ''
    routeCommandDirect(userMsg, { to, cfg: _replyCfg, event }).then(handled => {
      if (handled) {
        markHandledByDirect(userMsg)
        console.log(`[cc-soul][routeCommand] fallback to routeCommandDirect: handled`)
      }
    }).catch(() => {}) // intentionally silent — async command fallback
    ctx.bodyForAgent = '[系统] 命令已处理，结果已发送。'
    return true
  }

  // Not a command
  return false
}

// ═══════════════════════════════════════════════════════════════════════════════
// routeCommandDirect — read-only command handler (from context-engine assemble())
// ═══════════════════════════════════════════════════════════════════════════════

export async function routeCommandDirect(userMsg: string, params: any): Promise<boolean> {
  if (!userMsg) return false
  const _to = params?.to || ''
  const _cfg = params?.cfg || _replyCfg
  const _replyCallback = params?.replyCallback
  const reply = (text: string) => {
    if (typeof _replyCallback === 'function') _replyCallback(text)
    return replySender(_to, text, _cfg).catch(() => {}) // intentionally silent — reply delivery
  }

  // ── Help command override (different help text for direct path) ──
  if (/^(help|帮助|命令列表|commands)$/i.test(userMsg.trim())) {
    reply(HELP_TEXT_DIRECT)
    return true
  }

  // ── Registry-based matching (read + both commands only) ──
  const matched = matchCommand(userMsg, false)
  if (matched) {
    const cmdCtx: CommandContext = { senderId: '', channelId: '', session: {} as any, ctx: {}, event: params?.event }
    const result = matched.cmd.execute(matched.match, cmdCtx)
    const text = result instanceof Promise ? await result : result
    if (text != null) {
      reply(text)
      return true
    }
    // result === null means conditional command didn't match
  }

  // Not handled by routeCommandDirect — let inbound_claim pass it through
  return false
}

// ═══════════════════════════════════════════════════════════════════════════════
// INBOUND CLAIM — OpenClaw SDK integration (command detection + routing)
// ═══════════════════════════════════════════════════════════════════════════════

/** Command patterns — matches both routeCommand and routeCommandDirect triggers */
const CMD_PATTERNS = [
  /^(help|帮助|命令列表|commands)$/i,
  /^(搜索记忆|search memory)\s+/i,
  /^(我的记忆|my memories)$/i,
  /^(stats)$/i,
  /^(soul state|灵魂状态|内心状态)$/i,
  /^(情绪周报|mood report)$/i,
  /^(能力评分|capability)$/i,
  /^(功能状态|features)$/i,
  /^(记忆健康|memory health)$/i,
  /^(功能|feature)\s+/i,
  /^(人格列表|personas?)$/i,
  /^(导出|export)/i,
  /^(导入|import)/i,
  /^full backup$/i,
  /^(实验|experiment)/i,
  /^(tune|调整)/i,
  /^(ingest|导入文件)/i,
  /^(价值观|values)$/i,
  /^(cost|成本)$/i,
  /^(sync|同步)/i,
  /^(upgrade|更新)/i,
  /^(radar|竞品)/i,
  /^(dashboard|仪表盘|记忆地图|stats|soul state|灵魂状态|情绪周报|能力评分|metrics|cost)/i,
  /^(我的技能|my skills)$/i,
  /^(时间旅行|time travel)\s+/i,
  /^(推理链|reasoning chain)$/i,
  /^(情绪锚点|emotion anchors?)$/i,
  /^(记忆链路|memory chain)\s+/i,
  /^(保存话题|save topic)$/i,
  /^(切换话题|switch topic)\s+/i,
  /^(话题列表|topic list)$/i,
  /^(共享记忆|share memory)\s+/i,
  /^(私有记忆|private memory)\s+/i,
  /^(别记了?这[个条]?|别记住|don't remember|forget this|不要记)$/i,
]
const PRIVACY_TRIGGERS_RE = /^(别记了|隐私模式|privacy mode|可以了|关闭隐私|恢复记忆)$/i

/**
 * Check if a message is a cc-soul command (for inbound_claim filtering).
 */
export function isCommand(msg: string): boolean {
  const trimmed = (msg || '').trim()
  if (!trimmed) return false
  if (CMD_PATTERNS.some(p => p.test(trimmed))) return true
  if (PRIVACY_TRIGGERS_RE.test(trimmed)) return true
  return false
}

/**
 * Handle a command from inbound_claim hook.
 * Called when isCommand() returns true — routes to routeCommandDirect
 * with SDK config for replySender.
 */
async function handleCommandInbound(
  msg: string,
  to: string,
  cfg: any,
  event: any,
): Promise<boolean> {
  // Thread SDK config so cmdReply / replySender can use it
  setReplyCfg(cfg)
  try {
    const handled = await routeCommandDirect(msg.trim(), { to, cfg, event })
    if (handled) markHandledByDirect(msg)
    return handled
  } catch (e: any) {
    console.error(`[cc-soul][handleCommandInbound] error: ${e.message}`)
    return false
  }
}

// ── generateMemoryChain (inlined from deleted reports.ts) ──

function generateMemoryChain(keyword: string): string {
  const db = getDb()
  if (!db) return `🔗 记忆链路「${keyword}」\n数据库初始化中，请稍后重试。`
  const kw = `%${keyword.toLowerCase()}%`
  let memories: any[] = []
  try {
    memories = db.prepare(
      "SELECT content, scope, ts, tags FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND (LOWER(content) LIKE ? OR LOWER(tags) LIKE ?) ORDER BY ts ASC LIMIT 30"
    ).all(kw, kw) as any[]
  } catch { return `🔗 记忆链路「${keyword}」\n查询失败。` }
  if (memories.length === 0) return `🔗 记忆链路「${keyword}」\n没有找到相关记忆。`
  const lines: string[] = [`🔗 记忆链路「${keyword}」`]
  const scopeDepth: Record<string, number> = {
    'preference': 0, 'fact': 0, 'event': 0, 'topic': 0,
    'correction': 1, 'discovery': 1, 'proactive': 1,
    'reflection': 2, 'reflexion': 2,
  }
  let prevDate = ''
  for (const m of memories) {
    const date = new Date(m.ts).toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
    const depth = scopeDepth[m.scope] ?? 0
    const indent = '  '.repeat(depth)
    const connector = depth > 0 ? '└→ ' : ''
    const snippet = (m.content || '').slice(0, 50).replace(/\n/g, ' ')
    const dateTag = date !== prevDate ? ` (${date})` : ''
    prevDate = date
    lines.push(`  ${indent}${connector}[${snippet}${m.content.length > 50 ? '...' : ''}] ${m.scope}${dateTag}`)
  }
  return lines.join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTED FOR TESTING — command registry matching
// ═══════════════════════════════════════════════════════════════════════════════
export { matchCommand, COMMANDS }
export type { SoulCommand, CommandContext }
