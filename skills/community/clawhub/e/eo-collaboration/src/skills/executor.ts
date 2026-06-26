// ============================================================================
// EO Skill Executor - Unified skill invocation interface
// ============================================================================

import { skills, type SkillName, type SkillContext, type SkillResult } from './index.js'
import { EXPERTS } from '../experts/data.js'

// ---------------------------------------------------------------------------
// Plugin Context (extends SkillContext with plugin-level data)
// ---------------------------------------------------------------------------

export interface PluginContext extends SkillContext {
  pluginId: string
  userId?: string
  channel?: string
  workspace?: string
}

// ---------------------------------------------------------------------------
// Executor Options
// ---------------------------------------------------------------------------

export interface ExecuteOptions {
  skillName: SkillName
  args: string
  context: PluginContext
  /** Override default expert team (comma-separated expert IDs) */
  teamOverride?: string
  /** Timeout in ms (default: 300000) */
  timeoutMs?: number
}

// ---------------------------------------------------------------------------
// Executor Result
// ---------------------------------------------------------------------------

export interface ExecuteResult {
  success: boolean
  output: string
  skillName: SkillName
  durationMs: number
  expertUsed: string[]
  error?: string
}

// ---------------------------------------------------------------------------
// Default Logger
// ---------------------------------------------------------------------------

function createDefaultLogger() {
  return {
    info: (msg: string) => console.log(`[skill-executor] INFO: ${msg}`),
    warn: (msg: string) => console.warn(`[skill-executor] WARN: ${msg}`),
    error: (msg: string) => console.error(`[skill-executor] ERROR: ${msg}`),
  }
}

// ---------------------------------------------------------------------------
// Core Executor Function
// ---------------------------------------------------------------------------

/**
 * Execute a skill by name with the given arguments and context.
 *
 * Core logic:
 * 1. Validate skill exists in registry
 * 2. Resolve expert from skill definition
 * 3. Build execution context with runtime (subagent) + logger
 * 4. Call skill.execute() with parsed args
 * 5. Return structured result with timing and expert info
 */
export async function executeSkill(options: ExecuteOptions): Promise<ExecuteResult> {
  const { skillName, args, context, timeoutMs = 300000 } = options
  const logger = context.logger ?? createDefaultLogger()
  const startTime = Date.now()

  // 1. Validate skill
  const skill = skills[skillName]
  if (!skill) {
    return {
      success: false,
      output: '',
      skillName,
      durationMs: Date.now() - startTime,
      expertUsed: [],
      error: `Skill not found: ${skillName}. Available: ${Object.keys(skills).join(', ')}`,
    }
  }

  logger.info(`[execute-skill] Running skill="${skillName}" args="${args.slice(0, 50)}..."`)

  try {
    // 2. Build execution context
    const execContext: SkillContext = {
      runtime: context.runtime,
      logger,
      sessionId: context.sessionId,
    }

    // 3. Execute skill with timeout
    const result = await Promise.race([
      skill.execute(args, execContext),
      new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error(`Skill "${skillName}" timed out after ${timeoutMs}ms`)), timeoutMs)
      ),
    ])

    // 4. Resolve expert used
    const expertUsed = resolveExpert(skill.expert)

    const output = typeof result === 'string' ? result : (result as SkillResult).output ?? ''
    const success = typeof result === 'string' ? true : (result as SkillResult).success !== false

    logger.info(`[execute-skill] Completed skill="${skillName}" success=${success} durationMs=${Date.now() - startTime}`)

    return {
      success,
      output,
      skillName,
      durationMs: Date.now() - startTime,
      expertUsed,
    }
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err)
    logger.error(`[execute-skill] Failed skill="${skillName}" error="${errorMsg}"`)

    return {
      success: false,
      output: '',
      skillName,
      durationMs: Date.now() - startTime,
      expertUsed: [skill.expert],
      error: errorMsg,
    }
  }
}

// ---------------------------------------------------------------------------
// Batch Executor
// ---------------------------------------------------------------------------

/**
 * Execute multiple skills in parallel and aggregate results.
 */
export async function executeSkillsBatch(
  requests: Omit<ExecuteOptions, 'context'>[],
  context: PluginContext
): Promise<ExecuteResult[]> {
  return Promise.all(
    requests.map(req =>
      executeSkill({
        ...req,
        context,
      })
    )
  )
}

// ---------------------------------------------------------------------------
// Skill Router - Direct command-like invocation
// ---------------------------------------------------------------------------

/**
 * Simple command router that executes a skill by name with string args.
 * Convenience wrapper for command-style invocations.
 */
export async function routeSkillCommand(
  command: string,
  args: string,
  context: PluginContext
): Promise<string> {
  const skillName = command.toLowerCase() as SkillName

  if (!hasSkill(skillName)) {
    const available = Object.keys(skills)
    return `Unknown command: ${command}\n\nAvailable skills:\n${available
      .map(name => {
        const s = skills[name]
        return `- /${name}: ${s.description}`
      })
      .join('\n')}`
  }

  const result = await executeSkill({ skillName, args, context })

  if (!result.success) {
    return `❌ Skill "${skillName}" failed: ${result.error}\n\nOutput:\n${result.output}`
  }

  return result.output
}

// ---------------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------------

function resolveExpert(expertId: string): string[] {
  // Check if it's a role key in EXPERTS
  const expert = EXPERTS[expertId]
  if (expert) return [expert.name]

  // Check if it's a role category (architect, planner, etc.)
  const roleKey = expertId.toLowerCase()
  const matchingExperts = Object.values(EXPERTS).filter(e => e.role === roleKey)
  if (matchingExperts.length > 0) {
    return matchingExperts.map(e => e.name)
  }

  return [expertId]
}

function hasSkill(name: string): name is SkillName {
  return name in skills
}
