import type { SoulModule } from './brain.ts'

/**
 * tasks.ts — CLI task delegation, skill factory, planner, workflow
 *
 * Ported from handler.ts:
 * - Lines 1101-1214: CLI task delegation
 * - Lines 1715-1821: Skill factory (request pattern tracking)
 * - Lines 2153-2202: Planner (task decomposition)
 * - Lines 2204-2286: Workflow (multi-step automation)
 */

import { resolve } from 'path'

import type { PendingTask, RequestPattern, Plan, Workflow, InteractionStats } from './types.ts'
import { DATA_DIR, PATTERNS_PATH, PLANS_PATH, WORKFLOWS_PATH, loadJson, debouncedSave } from './persistence.ts'
import { spawnCLI } from './cli.ts'
import { addMemory } from './memory.ts'
import { notifySoulActivity } from './notify.ts'
import { extractJSON } from './utils.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

export const taskState = {
  pendingTasks: new Map<string, PendingTask>(),
  requestPatterns: [] as RequestPattern[],
  activePlans: [] as Plan[],
  workflows: [] as Workflow[],
}

export function initTasks() {
  taskState.requestPatterns = loadJson<RequestPattern[]>(PATTERNS_PATH, [])
  taskState.activePlans = loadJson<Plan[]>(PLANS_PATH, [])
  taskState.workflows = loadJson<Workflow[]>(WORKFLOWS_PATH, [])
  // Reload skills from disk (module-level load may have run before DATA_DIR was ready)
  skills = loadJson<Skill[]>(SKILLS_PATH, [])
  if (skills.length > 0) {
    console.log(`[cc-soul][skills] loaded ${skills.length} skills from disk`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLI TASK DELEGATION
// ═══════════════════════════════════════════════════════════════════════════════

export function detectActionIntent(userMsg: string, botResponse: string): boolean {
  // Response contains code block -> might need execution
  if (botResponse.includes('```') && botResponse.length > 200) return true
  // Response contains steps -> might need execution
  if (/\d+\.\s/.test(botResponse) && ['创建', '修改', '写入', '执行', '安装', '部署'].some(w => botResponse.includes(w))) return true
  // User explicitly asked for action
  if (['帮我做', '帮我写', '帮我改', '帮我创建', '帮我部署'].some(w => userMsg.includes(w))) return true
  return false
}

export function detectAndDelegateTask(userMsg: string, botResponse: string, event: any) {
  if (!detectActionIntent(userMsg, botResponse)) return

  const chatId = event.context?.conversationId || event.sessionKey || 'default'

  const taskDoc = [
    '# 任务',
    `用户需求: ${userMsg.slice(0, 500)}`,
    '',
    '# 方案',
    botResponse.slice(0, 1500),
    '',
    '# 要求',
    '按方案执行，完成后简要报告结果。',
  ].join('\n')

  taskState.pendingTasks.set(chatId, {
    taskDoc,
    userPrompt: userMsg.slice(0, 200),
    ts: Date.now(),
  })

  console.log(`[cc-soul][task] 检测到任务意图，等待确认: ${userMsg.slice(0, 40)}`)
}

export function checkTaskConfirmation(msg: string, chatId: string): boolean {
  const task = taskState.pendingTasks.get(chatId)
  if (!task) return false

  // Expire after 10 minutes
  if (Date.now() - task.ts > 600000) {
    taskState.pendingTasks.delete(chatId)
    return false
  }

  const m = msg.trim().toLowerCase()
  // Confirm words
  if (['做', '执行', '确认', '开始', 'go', 'ok', '好', '可以', '搞', '干', '行'].includes(m)) {
    executeCLITask(chatId, task)
    return true
  }
  // Cancel words
  if (['算了', '不用', '取消', '别做'].some(w => m.includes(w))) {
    taskState.pendingTasks.delete(chatId)
    console.log(`[cc-soul][task] 用户取消任务`)
    return false
  }

  return false
}

export function executeCLITask(chatId: string, task: PendingTask, stats?: InteractionStats, saveStats?: () => void) {
  taskState.pendingTasks.delete(chatId)
  console.log(`[cc-soul][task] 开始执行: ${task.userPrompt.slice(0, 40)}`)

  spawnCLI(task.taskDoc, (output) => {
    const result = output.slice(0, 2000)
    console.log(`[cc-soul][task] CLI 完成: ${result.slice(0, 80)}`)

    addMemory(`[已完成任务] ${task.userPrompt.slice(0, 60)} → ${result.slice(0, 100)}`, 'task')

    if (stats && saveStats) {
      stats.tasks++
      saveStats()
    }
  }, 120000, `task-${task.userPrompt.slice(0, 20)}`)
}

// ═══════════════════════════════════════════════════════════════════════════════
// SKILL FACTORY — auto-discover repeated patterns and suggest automation
// ═══════════════════════════════════════════════════════════════════════════════

export function trackRequestPattern(msg: string) {
  if (msg.length < 10) return

  const words = (msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
  if (words.length < 2) return

  for (const pattern of taskState.requestPatterns) {
    const overlap = pattern.keywords.filter(k => words.includes(k)).length
    const similarity = overlap / Math.max(pattern.keywords.length, words.length)
    if (similarity >= 0.4) {
      pattern.count++
      pattern.lastSeen = Date.now()
      pattern.example = msg.slice(0, 200)
      debouncedSave(PATTERNS_PATH, taskState.requestPatterns)
      return
    }
  }

  // New pattern
  taskState.requestPatterns.push({
    keywords: words.slice(0, 10),
    count: 1,
    lastSeen: Date.now(),
    example: msg.slice(0, 200),
    skillCreated: false,
  })

  if (taskState.requestPatterns.length > 100) {
    taskState.requestPatterns.sort((a, b) => b.count - a.count)
    taskState.requestPatterns = taskState.requestPatterns.slice(0, 80)
  }
  debouncedSave(PATTERNS_PATH, taskState.requestPatterns)
}

export function detectSkillOpportunity(msg: string): string | null {
  for (const pattern of taskState.requestPatterns) {
    if (pattern.skillCreated) continue
    if (pattern.count < 3) continue

    const words = (msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
    const overlap = pattern.keywords.filter(k => words.includes(k)).length
    if (overlap < 2) continue

    pattern.skillCreated = true
    debouncedSave(PATTERNS_PATH, taskState.requestPatterns)

    return `[技能建议] 你已经第${pattern.count}次处理类似请求了（如: "${pattern.example.slice(0, 40)}"）。` +
           `建议创建一个可复用的工具/脚本来自动化这类操作，下次直接用。`
  }
  return null
}

export function autoCreateSkill(description: string, example: string) {
  const prompt = [
    `请为以下重复性任务创建一个 bash 脚本或 Python 工具。`,
    ``,
    `任务描述: ${description}`,
    `示例请求: ${example}`,
    ``,
    `要求:`,
    `1. 创建可执行脚本`,
    `2. 保存到 ~/.openclaw/skills/ 目录`,
    `3. 添加使用说明`,
  ].join('\n')

  spawnCLI(prompt, (output) => {
    if (output) {
      addMemory(`[技能创建] ${description.slice(0, 60)} → ${output.slice(0, 100)}`, 'task')
      console.log(`[cc-soul][skill] created: ${description.slice(0, 40)}`)
      notifySoulActivity(`🔧 自创技能: ${description.slice(0, 40)}`).catch(() => {}) // intentionally silent
    }
  }, 60000, `skill-create-${description.slice(0, 20)}`)
}

// ═══════════════════════════════════════════════════════════════════════════════
// PLANNER — complex task decomposition
// ═══════════════════════════════════════════════════════════════════════════════

export function getActivePlanHint(): string {
  const active = taskState.activePlans.filter(p => Array.isArray(p.steps) && p.steps.some(s => s.status === 'pending' || s.status === 'running'))
  if (active.length === 0) return ''
  const latest = active[active.length - 1]
  const next = latest.steps.find(s => s.status === 'pending')
  if (!next) return ''
  return `[进行中的计划] ${latest.goal.slice(0, 40)} → 下一步: ${next.desc}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// WORKFLOW — multi-step automation
// ═══════════════════════════════════════════════════════════════════════════════

export function createWorkflow(name: string, trigger: string, steps: string[]) {
  if (taskState.workflows.some(w => w.name === name)) return
  taskState.workflows.push({ name, trigger, steps, lastRun: 0, runCount: 0 })
  if (taskState.workflows.length > 30) taskState.workflows = taskState.workflows.slice(-25)
  debouncedSave(WORKFLOWS_PATH, taskState.workflows)
  console.log(`[cc-soul][workflow] created: ${name} (${steps.length} steps)`)
  notifySoulActivity(`⚙️ 新工作流: ${name} (${steps.length}步)`).catch(() => {}) // intentionally silent
}

export function executeWorkflow(wf: Workflow) {
  wf.lastRun = Date.now()
  wf.runCount++
  debouncedSave(WORKFLOWS_PATH, taskState.workflows)

  let stepIdx = 0
  function runNextStep() {
    if (stepIdx >= wf.steps.length) {
      console.log(`[cc-soul][workflow] ${wf.name} completed (${wf.steps.length} steps)`)
      notifySoulActivity(`✅ 工作流完成: ${wf.name}`).catch(() => {}) // intentionally silent
      addMemory(`[工作流完成] ${wf.name}`, 'task')
      return
    }
    const step = wf.steps[stepIdx]
    console.log(`[cc-soul][workflow] ${wf.name} step ${stepIdx + 1}/${wf.steps.length}: ${step.slice(0, 40)}`)
    spawnCLI(step, (output) => {
      addMemory(`[工作流步骤] ${wf.name} #${stepIdx + 1}: ${output.slice(0, 80)}`, 'task')
      stepIdx++
      setTimeout(runNextStep, 2000)
    })
  }
  runNextStep()
}

export function detectWorkflowTrigger(msg: string): Workflow | null {
  for (const wf of taskState.workflows) {
    const triggerWords = wf.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []
    const msgWords = msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []
    const overlap = triggerWords.filter(w => msgWords.some(m => m.toLowerCase() === w.toLowerCase())).length
    if (overlap >= 2) return wf
  }
  return null
}

// ═══════════════════════════════════════════════════════════════════════════════
// Skill Library — save verified solutions for reuse (Voyager-inspired)
// ═══════════════════════════════════════════════════════════════════════════════

interface Skill {
  name: string
  description: string      // what problem this solves
  solution: string         // the actual solution (code, steps, etc.)
  keywords: string[]       // for retrieval
  verified: boolean        // user confirmed it works
  usedCount: number
  createdAt: number
  lastUsed: number
}

const SKILLS_PATH = resolve(DATA_DIR, 'skills.json')
let skills: Skill[] = loadJson<Skill[]>(SKILLS_PATH, [])

function saveSkills() {
  debouncedSave(SKILLS_PATH, skills)
}

/** Save a new skill from a successful interaction */
export function saveSkill(name: string, description: string, solution: string, keywords: string[]) {
  // Dedup
  if (skills.some(s => s.name === name)) return

  skills.push({
    name,
    description,
    solution: solution.slice(0, 2000),
    keywords: keywords.map(k => k.toLowerCase()),
    verified: false,
    usedCount: 0,
    createdAt: Date.now(),
    lastUsed: 0,
  })

  if (skills.length > 100) {
    skills.sort((a, b) => b.usedCount - a.usedCount)
    skills = skills.slice(0, 80)
  }
  saveSkills()
  console.log(`[cc-soul][skills] saved: ${name}`)
}

/** Find relevant skills for current query */
export function findSkills(msg: string, topN = 2): Skill[] {
  if (skills.length === 0) return []
  const lower = msg.toLowerCase()

  const scored = skills.map(s => {
    const keywordHits = s.keywords.filter(k => lower.includes(k)).length
    const descHits = (s.description.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || [])
      .filter(w => lower.includes(w.toLowerCase())).length
    return { skill: s, score: keywordHits * 2 + descHits }
  }).filter(s => s.score > 0)

  scored.sort((a, b) => b.score - a.score)

  const results = scored.slice(0, topN).map(s => {
    s.skill.usedCount++
    s.skill.lastUsed = Date.now()
    return s.skill
  })

  if (results.length > 0) saveSkills()
  return results
}

/** Auto-extract skills from successful task completions */
export function autoExtractSkill(userMsg: string, botResponse: string) {
  // Only extract if response contains code blocks (likely a solution)
  if (!botResponse.includes('```') || botResponse.length < 100) return
  if (userMsg.length < 10) return

  spawnCLI(
    `以下对话包含一个技术问题的解决方案。判断是否值得保存为可复用技能。\n\n` +
    `问题: "${userMsg.slice(0, 200)}"\n` +
    `方案: "${botResponse.slice(0, 500)}"\n\n` +
    `如果值得保存，输出JSON: {"name":"技能名","description":"解决什么问题","keywords":["关键词"],"solution":"核心方案(简化版)"}\n` +
    `如果不值得（太具体/一次性），回答"否"`,
    (output) => {
      if (!output || output.includes('否')) return
      try {
        const match = output.match(/\{[\s\S]*\}/)
        if (match) {
          const skill = JSON.parse(match[0])
          if (skill.name && skill.solution) {
            saveSkill(skill.name, skill.description || '', skill.solution, skill.keywords || [])
          }
        }
      } catch { /* ignore parse errors */ }
    }
  )
}

export { skills as skillLibrary }

// ═══════════════════════════════════════════════════════════════════════════════
// AUTONOMOUS TASK LOOP — goal → decompose → execute → evaluate → next
// ═══════════════════════════════════════════════════════════════════════════════

interface AutonomousGoal {
  id: string
  goal: string
  steps: { desc: string; status: 'pending' | 'running' | 'done' | 'failed'; result?: string }[]
  createdAt: number
  completedAt: number
  maxRetries: number
  currentStep: number
  evaluation: string
}

const GOALS_PATH = resolve(DATA_DIR, 'goals.json')
let activeGoals: AutonomousGoal[] = loadJson<AutonomousGoal[]>(GOALS_PATH, [])
  .filter(g => Array.isArray(g.steps)) // sanitize: drop corrupt entries with missing steps

function saveGoals() {
  debouncedSave(GOALS_PATH, activeGoals)
}

/**
 * Start an autonomous goal: decompose → execute step by step.
 * Called when user gives a high-level objective.
 */
export function startAutonomousGoal(goal: string, callback?: (result: string) => void) {
  console.log(`[cc-soul][goal] starting: ${goal.slice(0, 60)}`)

  // Step 1: Decompose via CLI
  spawnCLI(
    `Break this goal into 3-7 concrete executable steps. Each step should be a single actionable task.\n\n` +
    `Goal: "${goal}"\n\n` +
    `Format: one step per line, just the action (no numbering, no explanation).`,
    (output) => {
      if (!output) {
        if (callback) callback('Failed to decompose goal')
        return
      }

      const steps = output.split('\n')
        .map(l => l.replace(/^\d+[.)\s]+/, '').trim())
        .filter(l => l.length > 5)
        .map(desc => ({ desc, status: 'pending' as const, result: undefined }))

      if (steps.length < 2) {
        if (callback) callback('Could not break goal into steps')
        return
      }

      const goalObj: AutonomousGoal = {
        id: Date.now().toString(36),
        goal,
        steps,
        createdAt: Date.now(),
        completedAt: 0,
        maxRetries: 2,
        currentStep: 0,
        evaluation: '',
      }

      activeGoals.push(goalObj)
      if (activeGoals.length > 10) activeGoals = activeGoals.slice(-8)
      saveGoals()

      console.log(`[cc-soul][goal] decomposed into ${steps.length} steps`)

      // Start executing
      executeNextStep(goalObj, callback)
    }
  )
}

/**
 * Execute the next pending step in a goal.
 */
function executeNextStep(goal: AutonomousGoal, callback?: (result: string) => void) {
  const step = goal.steps.find(s => s.status === 'pending')
  if (!step) {
    // All steps done — evaluate
    evaluateGoal(goal, callback)
    return
  }

  const stepIdx = goal.steps.indexOf(step)
  step.status = 'running'
  goal.currentStep = stepIdx
  saveGoals()

  console.log(`[cc-soul][goal] executing step ${stepIdx + 1}/${goal.steps.length}: ${step.desc.slice(0, 50)}`)

  // Previous steps context
  const prevResults = goal.steps
    .filter(s => s.status === 'done' && s.result)
    .map((s, i) => `Step ${i + 1}: ${s.desc} → ${s.result}`)
    .join('\n')

  const prompt = prevResults
    ? `Previous steps completed:\n${prevResults}\n\nNow execute this step:\n"${step.desc}"\n\nDo it and report the result briefly.`
    : `Execute this step:\n"${step.desc}"\n\nDo it and report the result briefly.`

  spawnCLI(prompt, (output) => {
    if (output && output.length > 5) {
      step.status = 'done'
      step.result = output.slice(0, 500)
      console.log(`[cc-soul][goal] step ${stepIdx + 1} done: ${output.slice(0, 60)}`)
    } else {
      step.status = 'failed'
      step.result = 'No output'
      console.log(`[cc-soul][goal] step ${stepIdx + 1} failed`)
    }

    saveGoals()

    // Continue to next step (with delay to not overwhelm CLI)
    setTimeout(() => executeNextStep(goal, callback), 3000)
  }, 60000) // 60s per step
}

/**
 * Evaluate the completed goal: did we achieve what was asked?
 */
function evaluateGoal(goal: AutonomousGoal, callback?: (result: string) => void) {
  const stepResults = goal.steps
    .map((s, i) => `${i + 1}. ${s.desc} → ${s.status === 'done' ? s.result : 'FAILED'}`)
    .join('\n')

  spawnCLI(
    `Evaluate this completed goal:\n\nGoal: "${goal.goal}"\n\nSteps and results:\n${stepResults}\n\n` +
    `Was the goal achieved? Rate 1-10 and explain in 1 sentence.`,
    (output) => {
      goal.evaluation = output?.slice(0, 200) || 'No evaluation'
      goal.completedAt = Date.now()
      saveGoals()

      // Store result as memory
      addMemory(
        `[goal completed] ${goal.goal} → ${goal.evaluation}`,
        'task', undefined, 'global'
      )

      const summary = `Goal "${goal.goal.slice(0, 40)}": ${goal.steps.filter(s => s.status === 'done').length}/${goal.steps.length} steps done. ${goal.evaluation}`
      console.log(`[cc-soul][goal] ${summary}`)

      if (callback) callback(summary)
    }
  )
}

/**
 * Get active goal status for augment injection.
 */
export function getActiveGoalHint(): string {
  const active = activeGoals.find(g => !g.completedAt && Array.isArray(g.steps) && g.steps.some(s => s.status === 'pending' || s.status === 'running'))
  if (!active) return ''

  const done = active.steps.filter(s => s.status === 'done').length
  const total = active.steps.length
  const next = active.steps.find(s => s.status === 'pending')

  return `[Active Goal] "${active.goal.slice(0, 40)}" — ${done}/${total} steps done${next ? `. Next: ${next.desc.slice(0, 40)}` : ''}`
}

/**
 * Detect if user message is a high-level goal request.
 */
export function detectGoalIntent(msg: string): boolean {
  const m = msg.toLowerCase()
  // Goal indicators: multi-step requests, ambitious asks
  return (
    ['goal:', 'objective:', 'mission:', '目标:', '目标是'].some(w => m.includes(w)) ||
    (m.includes('帮我') && m.length > 50) ||
    (m.includes('help me') && m.length > 50)
  )
}

export function detectWorkflowOpportunity(msg: string, response: string) {
  const stepIndicators = response.match(/\d+\.\s/g)
  if (!stepIndicators || stepIndicators.length < 3) return

  spawnCLI(
    `以下回复包含多步操作。判断这是否适合变成一个可复用的工作流？\n\n` +
    `用户: ${msg.slice(0, 200)}\n回复: ${response.slice(0, 500)}\n\n` +
    `如果适合，输出JSON: {"name":"工作流名","trigger":"触发条件","steps":["步骤1","步骤2"]}\n如果不适合，回答"否"`,
    (output) => {
      try {
        const result = extractJSON(output)
        if (result && result.name && result.steps?.length >= 2) {
          createWorkflow(result.name, result.trigger || msg.slice(0, 50), result.steps)
        }
      } catch (e: any) { console.error(`[cc-soul] JSON parse error: ${e.message}`) }
    }
  )
}

export const tasksModule: SoulModule = {
  id: 'tasks',
  name: '任务系统',
  dependencies: ['memory'],
  priority: 50,
  init() { initTasks() },
}
