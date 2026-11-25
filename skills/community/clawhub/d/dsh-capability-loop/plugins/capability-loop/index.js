/**
 * dsh-capability-loop-bundle — 接管插件（host half）
 *
 * 作用：在**已标记工程**（`.dsh/loop/project.json` 存在）的会话首个 `agent/pre-step`
 * 上，把一小段治理契约折进该步消息，从而让「闭环」不依赖模型自觉加载 skill。
 *
 * 档位来自 `.dsh/loop/state.json` 的 `mode`（缺省用 `defaultMode`）：
 *   off    → 不注入
 *   shadow → 一行提示（只记录、不阻断）
 *   on     → 完整契约（≤ maxContractChars）
 *
 * 纪律：
 *   - **fail-open**：任何读文件/解析/构造失败都不影响对话，只记日志。
 *   - **幂等**：resume/fork 后按会话历史里已有的注入（source.kind + digest）去重。
 *   - **只读 state.json**：唯一写入方是 skill 的脚本；本插件只写 `.dsh/loop/shadow-log.jsonl`。
 *   - 不新增 Session 事件类型（只用普通 `user/message`），避免会话无法重开。
 *
 * 依据（已核源码，DSH 0.2.2-rc.3）：
 *   - `agent/pre-step` 瀑布签名：`@deepseek-ai/dsh-agent/src/runtime-types.ts` L351
 *   - `decision.messages` 折叠方式：`@deepseek-ai/dsh-agent-instructions/src/index.ts` L330-356
 *   - `createUserMessage`：`@deepseek-ai/dsh-llm/src/message.ts` L246（`MessageSourceMap` 为 merge-extensible，未知 kind 消费者降级）
 *   - 手工构造 UserMessage 的先例（无需导入）：`@deepseek-ai/dsh-session/src/repair.ts` L168
 *   - `ctx.workingDirectory.ensure(agent, signal)`：`dsh-working-directory/src/index.ts` L192
 *   - `ctx.fs.resolve/stat/readText/writeText`：`dsh-fs/src/index.ts` L149/L198/L222/L283
 *
 * 为什么**不**在模块顶层 `import '@deepseek-ai/dsh-llm'`：本机目录安装（`install_bundle` 走
 * pnpm link）时，插件的真实路径在工作区，Node 解析不会走到 profile 的 node_modules，
 * 顶层 import 会 `ERR_MODULE_NOT_FOUND` 导致整行不激活。改为运行时动态解析 + 手工构造兜底：
 * 能解析就用官方 `createUserMessage`，解析不到就按 `repair.ts` 同款形状手工构造。
 */

import { executeAction } from './actions.js'

export const name = 'capability-loop-takeover'

/** 没有 fs / workingDirectory 的 profile 里保持不激活（不抛错）。 */
export const inject = ['fs', 'workingDirectory']

const SOURCE_KIND = 'capability-loop'
const STATE_REL = '.dsh/loop/state.json'
const PROJECT_REL = '.dsh/loop/project.json'
const SHADOW_LOG_REL = '.dsh/loop/shadow-log.jsonl'

const STAGE_INDEX = {
  INTAKE: 1, AUDIT: 2, FIX: 3, WIRE: 4, HANDOFF: 5, GRILL: 6, GATE: 7,
}

const STAGE_EXIT = {
  INTAKE: 'docs/loop/project-profile.md 已产出（六问答案 + 真相源 + 目标与验收）',
  AUDIT: '体检报告已落盘（九组指标 + 与上次的漂移对比）',
  FIX: '修复走 DryRun → apply → verify，并留备份路径',
  WIRE: 'design-context.md 已取证；loop-gate -Kind design 退出码 0；grill 至少 1 条打回并修正',
  HANDOFF: 'docs/handoff/<slug>/ 四件套齐全；handoff-audit.py 退出码 0',
  GRILL: 'grill-*.md 已记录（≥1 个打回并修正）',
  GATE: 'loop-gate 全绿；CHANGELOG/version.json 已 bump',
}

const CHECK_LABEL = {
  design: '设计门',
  requirement: '需求门',
  test: '测试门',
  handoff: '交接体检',
  grill: 'grill',
  environment: '环境验收',
  'environment-audit': '能力体检',
}

function clip(text, max) {
  if (typeof text !== 'string') return ''
  const limit = typeof max === 'number' && max > 0 ? max : 0
  if (limit === 0 || text.length <= limit) return text
  return text.slice(0, Math.max(0, limit - 12)) + '…（已截断）'
}

/** 手工构造 UserMessage（形状与 `dsh-session/src/repair.ts` 的合成消息一致）。 */
let fallbackSeq = 0
function manualUserMessage(input) {
  fallbackSeq += 1
  return Object.freeze({
    id: 'capability-loop-' + fallbackSeq + '-' + Date.now().toString(36),
    role: 'user',
    content: input.content,
    source: input.source,
  })
}

/**
 * 解析「造 UserMessage」的实现：优先官方 `createUserMessage`，解析不到就用手工构造。
 * 只在第一次注入时尝试一次；结果缓存（成功/失败都缓存，避免每步重复失败）。
 */
let messageFactory
async function resolveMessageFactory(warn) {
  if (messageFactory !== undefined) return messageFactory
  try {
    const mod = await import('@deepseek-ai/dsh-llm')
    if (mod !== null && mod !== undefined && typeof mod.createUserMessage === 'function') {
      messageFactory = mod.createUserMessage
      return messageFactory
    }
  } catch (error) {
    warn('无法解析 @deepseek-ai/dsh-llm，回退为手工构造 UserMessage', error)
  }
  messageFactory = manualUserMessage
  return messageFactory
}

/** 轻量指纹：只用于「同内容不重复注入」，不作安全用途。 */
function digestOf(text) {
  let h = 5381
  for (let i = 0; i < text.length; i += 1) {
    h = ((h << 5) + h + text.charCodeAt(i)) | 0
  }
  return 'cl' + (h >>> 0).toString(16) + '-' + text.length.toString(16)
}

function parseJson(text) {
  try {
    return JSON.parse(text)
  } catch {
    return null
  }
}

function isFileInfo(info) {
  return info !== undefined && info !== null && info.type === 'file'
}

/** 读工作区内的 JSON 文件；不存在/非文件/解析失败都返回 null（fail-open）。 */
async function readJson(ctx, cwd, rel, signal) {
  const fsService = ctx.get('fs')
  if (fsService === undefined) return null
  try {
    const target = await fsService.resolve(rel, { cwd, signal })
    const info = await fsService.stat(target, signal)
    if (!isFileInfo(info)) return null
    return parseJson(await fsService.readText(target, signal))
  } catch {
    return null
  }
}

function pickNext(state) {
  if (state === null || typeof state !== 'object') return null
  const next = state.next
  if (next === null || typeof next !== 'object') return null
  const label = typeof next.label === 'string' ? next.label.trim() : ''
  const command = typeof next.command === 'string' ? next.command.trim() : ''
  if (label === '' && command === '') return null
  return { label, command }
}

function summarizeChecks(state) {
  if (state === null || typeof state !== 'object') return []
  const checks = state.checks
  if (checks === null || typeof checks !== 'object') return []
  const rows = []
  for (const key of Object.keys(checks)) {
    const entry = checks[key]
    if (entry === null || typeof entry !== 'object') continue
    const status = typeof entry.status === 'string' ? entry.status : '?'
    rows.push((CHECK_LABEL[key] || key) + '=' + status)
  }
  return rows
}

function summarizeBlockers(state) {
  if (state === null || typeof state !== 'object') return []
  const list = state.blockers
  if (!Array.isArray(list)) return []
  const rows = []
  for (const item of list.slice(0, 3)) {
    if (item === null || typeof item !== 'object') continue
    const id = typeof item.id === 'string' ? item.id : 'D-?'
    const text = typeof item.text === 'string' ? item.text.trim() : ''
    if (text === '') continue
    rows.push(id + ' ' + text)
  }
  return rows
}

/** on 档：完整契约（≤ maxContractChars）。 */
function buildContract(state, project, cfg, skillDir) {
  const hasState = state !== null && typeof state === 'object'
  const stage = hasState && typeof state.stage === 'string' && STAGE_INDEX[state.stage] ? state.stage : 'INTAKE'
  const index = STAGE_INDEX[stage] || 1
  const name = project !== null && typeof project.name === 'string' && project.name.trim() !== ''
    ? project.name.trim()
    : '本工程'
  const version = hasState && typeof state.skillVersion === 'string' ? state.skillVersion : 'unknown'
  const next = hasState ? pickNext(state) : null
  const checks = hasState ? summarizeChecks(state) : []
  const blockers = hasState ? summarizeBlockers(state) : []

  const lines = [
    '<system-reminder>',
    '[capability-loop v' + version + '] 本工程（' + name + '）已启用治理闭环；当前阶段 '
      + stage + '（第 ' + index + '/7 阶段）。',
    '适用：需求/方案、设计/改版、实现与交接、测试与验收、复盘。豁免：只读问答、单文件小改（≤30 分钟）、纯闲聊——直接做，不套流程。',
    '',
    '硬约束：',
    '1. 未完成 INTAKE（.dsh/loop/project-profile.md）不得进入实现；新项目/新模块/跨模块改动才做完整六问，小改只问目标/验收/影响面。',
    '2. 说“完成/已修复/已通过”必须附证据：命令 + 退出码 + 关键输出或截图；拿不到实测就写“未实测 + 原因 + 补测方式”。',
    '3. PASS 不得由写的人自己给；终门要有他人的评审记录。',
    '4. 交付/交接前必须 grill（记录 grill-*.md）；硬门用 loop-gate.ps1 -RequireGrill。',
    '5. 改本 skill 必须在同一提交 bump version.json + CHANGELOG.md。',
    '6. 门禁 FAIL 时只能说“未通过 + 缺什么”，不得改写结论。',
    '',
    '本阶段出口：' + (STAGE_EXIT[stage] || '按七阶段纪律取证'),
  ]
  if (checks.length > 0) lines.push('当前门禁：' + checks.join(' · '))
  if (blockers.length > 0) lines.push('阻断：' + blockers.join('；'))
  if (next !== null) {
    lines.push('下一步：' + (next.label || '按 state.next 执行')
      + (next.command !== '' ? '（命令：' + next.command + '）' : ''))
  }
  if (skillDir !== '') lines.push('需要细节再读：' + skillDir + '/references/02-takeover.md（只读这一篇，不整包加载）。')
  lines.push('状态源：' + STATE_REL + '（用户可在“能力闭环”面板查看）。')
  lines.push('</system-reminder>')

  return clip(lines.join('\n'), cfg.maxContractChars)
}

/** shadow 档：一行提示，只记录不阻断。超预算时先丢「下一步」，不截断成半句。 */
function buildShadowNotice(state, cfg) {
  const hasState = state !== null && typeof state === 'object'
  const stage = hasState && typeof state.stage === 'string' ? state.stage : ''
  const next = hasState ? pickNext(state) : null
  const base = '[capability-loop · 影子] 本工程已记录治理状态（' + STATE_REL + '）'
    + (stage !== '' ? '，阶段 ' + stage : '')
    + '。只记录、不阻断；门禁失败不会拦住对话'
  const limit = typeof cfg.maxShadowChars === 'number' && cfg.maxShadowChars > 0 ? cfg.maxShadowChars : 140
  if (next !== null && next.label !== '') {
    const withTail = base + '；参考下一步：' + next.label + '。'
    if (withTail.length <= limit) return withTail
  }
  const plain = base + '。'
  return plain.length <= limit ? plain : clip(plain, limit)
}

/** 会话历史里是否已有同样内容的注入（resume/fork 去重）。 */
function alreadyInjected(agent, digest) {
  const session = agent !== null && agent !== undefined ? agent.session : undefined
  if (session === undefined || session === null) return false
  const surface = session.surface
  if (surface === undefined || surface === null) return false
  const nodes = surface.nodes
  if (nodes === undefined || nodes === null || nodes.length === 0) return false
  let scanned = 0
  for (let i = nodes.length - 1; i >= 0 && scanned < 200; i -= 1, scanned += 1) {
    let event
    try {
      event = session.eventAt(nodes[i])
    } catch {
      continue
    }
    if (event === undefined || event === null || event.type !== 'user/message') continue
    const source = event.data !== null && event.data !== undefined ? event.data.source : undefined
    if (source !== undefined && source !== null && source.kind === SOURCE_KIND && source.digest === digest) {
      return true
    }
  }
  return false
}

/** 本批已认领的消息里是否已有同 digest 的注入。 */
function inBatch(messages, digest) {
  if (!Array.isArray(messages)) return false
  for (const message of messages) {
    const source = message !== null && message !== undefined ? message.source : undefined
    if (source !== undefined && source !== null && source.kind === SOURCE_KIND && source.digest === digest) {
      return true
    }
  }
  return false
}

/** 记录影子观察：每个会话一行，供 `loop-state.ps1 -Action sync-shadow` 计数。尽力而为。 */
async function logShadowSession(ctx, cwd, agent, signal, warn) {
  const fsService = ctx.get('fs')
  if (fsService === undefined) return
  const session = agent !== null && agent !== undefined ? agent.session : undefined
  const header = session !== undefined && session !== null ? session.header : undefined
  const sessionId = header !== undefined && header !== null ? String(header.id) : ''
  if (sessionId === '') return
  try {
    const target = await fsService.resolve(SHADOW_LOG_REL, { cwd, signal })
    const info = await fsService.stat(target, signal)
    let existing = ''
    if (isFileInfo(info)) {
      try {
        existing = await fsService.readText(target, signal)
      } catch {
        existing = ''
      }
    }
    if (existing.indexOf(sessionId) !== -1) return
    const line = JSON.stringify({ session: sessionId, at: new Date().toISOString() }) + '\n'
    // writeText(target, content, expected?, signal?, sandboxPolicy?)
    // 传**本会话自己的**沙箱策略：read-only 会话里写入会被拒（我们只 warn 不阻断，尊重用户沙箱），
    // workspace-write 会话里目标在工程内即可写，danger-full-access 不限制。
    let policy
    const policyService = ctx.get('sandboxPolicy')
    if (policyService !== undefined && policyService !== null && typeof policyService.resolve === 'function') {
      try {
        policy = policyService.resolve({ session })
      } catch {
        policy = undefined
      }
    }
    await fsService.writeText(target, existing + line, undefined, signal, policy)
  } catch (error) {
    // 影子日志是尽力而为：失败不影响注入，但要留日志便于排查（曾因静默吞错导致「注入成功但没记账」）。
    if (typeof warn === 'function') warn('影子日志写入失败（不影响注入）', error)
  }
}

export function apply(ctx, config) {
  const cfg = {
    defaultMode: 'off',
    maxContractChars: 1600,
    maxShadowChars: 140,
    shadowLog: true,
    debug: false,
    skillDir: '',
    pythonExecutable: '',
    workspaceRoot: '',
    ...(config !== null && config !== undefined ? config : {}),
  }
  if (cfg.defaultMode !== 'off' && cfg.defaultMode !== 'shadow' && cfg.defaultMode !== 'on') {
    cfg.defaultMode = 'off'
  }
  const skillDir = typeof cfg.skillDir === 'string' ? cfg.skillDir.trim().replace(/[\\/]+$/, '') : ''

  const log = (message) => {
    if (cfg.debug && ctx.logger !== undefined && typeof ctx.logger.info === 'function') {
      ctx.logger.info('[capability-loop] ' + message)
    }
  }
  const warn = (message, error) => {
    if (ctx.logger !== undefined && typeof ctx.logger.warn === 'function') {
      const detail = error !== null && error !== undefined && error.message !== undefined ? String(error.message) : String(error)
      ctx.logger.warn('[capability-loop] ' + message + (error !== undefined ? '：' + detail : ''))
    }
  }

  /** 计算本步该注入的内容；不需要注入返回 null。 */
  const compose = async (agent, signal) => {
    const cwd = await ctx.workingDirectory.ensure(agent, signal)
    const project = await readJson(ctx, cwd, PROJECT_REL, signal)
    if (project === null) return null // 未标记工程：零注入、零成本
    const state = await readJson(ctx, cwd, STATE_REL, signal)

    let mode = cfg.defaultMode
    const projectMode = project.mode
    if (projectMode === 'off' || projectMode === 'shadow' || projectMode === 'on') mode = projectMode
    const stateMode = state !== null && typeof state === 'object' ? state.mode : undefined
    if (stateMode === 'off' || stateMode === 'shadow' || stateMode === 'on') mode = stateMode
    if (mode === 'off') return { mode, text: null, cwd, state }

    if (mode === 'shadow') {
      if (cfg.shadowLog) await logShadowSession(ctx, cwd, agent, signal, warn)
      return { mode, text: buildShadowNotice(state, cfg), cwd, state }
    }
    return { mode, text: buildContract(state, project, cfg, skillDir), cwd, state }
  }

  ctx.on('agent/pre-step', async (payload, next) => {
    const decision = await next()
    try {
      if (decision === undefined || decision === null || decision.kind !== 'enter') return decision
      const agent = payload.agent
      if (agent === undefined || agent === null) return decision

      const composed = await compose(agent, payload.signal)
      if (composed === null || composed.text === null || composed.text === '') return decision

      const digest = digestOf(composed.mode + '|' + composed.text)
      if (inBatch(decision.messages, digest)) return decision
      if (alreadyInjected(agent, digest)) {
        log('history already holds this injection; skip')
        return decision
      }

      const make = await resolveMessageFactory(warn)
      const message = make({
        content: [{ type: 'text', text: composed.text }],
        source: {
          kind: SOURCE_KIND,
          form: 'instructions',
          mode: composed.mode,
          digest,
        },
      })

      // 折进本步批次：紧跟最后一条「本步认领的消息」，让用户直接提问先出现。
      const claimed = Array.isArray(payload.messages) ? payload.messages : []
      let lastClaimed = -1
      for (let i = decision.messages.length - 1; i >= 0; i -= 1) {
        if (claimed.indexOf(decision.messages[i]) !== -1) {
          lastClaimed = i
          break
        }
      }
      const messages = decision.messages.slice()
      if (lastClaimed >= 0) messages.splice(lastClaimed + 1, 0, message)
      else messages.push(message)

      log('inject mode=' + composed.mode + ' chars=' + composed.text.length + ' digest=' + digest)
      return { ...decision, messages }
    } catch (error) {
      // fail-open：治理不能把对话弄挂
      warn('注入失败（已降级为不注入）', error)
      return decision
    }
  })

  // ---------------- 运行中心：会话命令通道 ----------------
  // 客户端面板用 `ctx.remote.commands.execute(sessionId, '/capability-loop run gate …')` 触发；
  // 白名单与参数校验在 actions.js，绝不拼 shell。
  ctx.inject(['commands'], (scoped) => {
    scoped.effect(() => scoped.commands.register({
      name: 'capability-loop',
      description: '能力闭环：运行门禁/体检/交接体检/预检/打包/视觉探测/切档位（面板按钮走同一实现）',
      input: { hint: 'run gate kind=design taskDir=docs/design | mode on' },
      handler: async ({ agent, rawInput, signal }) => {
        const root = cfg.workspaceRoot !== '' ? cfg.workspaceRoot : cwdOf(agent)
        if (root === '') {
          return {
            kind: 'error',
            text: '拿不到会话工作目录：请在 Plugin 配置里填 workspaceRoot，或在一个有工作区的会话里执行。'
              + '（不猜进程 cwd，避免把门禁/打包跑错工程）',
          }
        }
        const outcome = await executeAction(ctx, { ...cfg, workspaceRoot: root }, rawInput, signal)
        if (signal !== undefined && signal.aborted) return { kind: 'error', text: '已取消' }
        return { kind: outcome.ok ? 'success' : 'error', text: outcome.text }
      },
    }))
  })
}

/** 取会话工作目录（命令 handler 只有 agent）；拿不到返回 ''（不猜进程 cwd）。 */
function cwdOf(agent) {
  const session = agent !== undefined && agent !== null ? agent.session : undefined
  const header = session !== undefined && session !== null ? session.header : undefined
  const cwd = header !== undefined && header !== null && typeof header.cwd === 'string' ? header.cwd : ''
  return cwd
}
