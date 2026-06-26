// ============================================================================
// EO Skills Registry - Central registration for all .ts Skills
// ============================================================================

import { planSkill, type PlanSkillContext, type PlanSkillResult } from './plan-skill.js'
import { architectSkill, type ArchitectSkillContext, type ArchitectSkillResult } from './architect-skill.js'
import { verifySkill, type VerifySkillContext, type VerifySkillResult } from './verify-skill.js'
import { codeReviewSkill, type CodeReviewSkillContext, type CodeReviewSkillResult } from './code-review-skill.js'

// ---------------------------------------------------------------------------
// Skill Registry
// ---------------------------------------------------------------------------

export interface EOSkill {
  name: string
  description: string
  expert: string
  role: string
  execute(
    args: string,
    context: SkillContext
  ): Promise<SkillResult>
}

export interface SkillContext {
  runtime: {
    subagent: {
      run: (params: {
        sessionKey: string
        message: string
        extraSystemPrompt?: string
        provider?: string
        model?: string
      }) => Promise<{ runId: string }>
      waitForRun: (params: { runId: string; timeoutMs?: number }) => Promise<{ status: string; error?: string }>
      getSessionMessages: (params: { sessionKey: string; limit?: number }) => Promise<{ messages: unknown[] }>
    }
  }
  logger: { info: (msg: string) => void; warn: (msg: string) => void; error: (msg: string) => void }
  sessionId?: string
}

export interface SkillResult {
  success: boolean
  output: string
  durationMs: number
  error?: string
}

// ---------------------------------------------------------------------------
// Registered Skills
// ---------------------------------------------------------------------------

export const skills: Record<string, EOSkill> = {
  plan: planSkill,
  architect: architectSkill,
  verify: verifySkill,
  'code-review': codeReviewSkill,
}

// ---------------------------------------------------------------------------
// Skill Names
// ---------------------------------------------------------------------------

export type SkillName = keyof typeof skills

export const SKILL_NAMES: readonly SkillName[] = ['plan', 'architect', 'verify', 'code-review']

// ---------------------------------------------------------------------------
// Skill Metadata
// ---------------------------------------------------------------------------

export const SKILL_META: Record<SkillName, { description: string; expert: string; icon: string }> = {
  plan: {
    description: 'Create a structured project plan with WBS, milestones, and expert team analysis',
    expert: 'planner',
    icon: '📋',
  },
  architect: {
    description: 'Design system architecture with technology stack, modules, and risk assessment',
    expert: 'architect',
    icon: '🏗️',
  },
  verify: {
    description: 'Verify implementation against specifications using checkpoint-based validation',
    expert: 'qa',
    icon: '✅',
  },
  'code-review': {
    description: 'Review code for quality, security, and best practices using multiple expert perspectives',
    expert: 'reviewer',
    icon: '🔍',
  },
}

// ---------------------------------------------------------------------------
// Context Type Exports (for command handlers)
// ---------------------------------------------------------------------------

export type { PlanSkillContext, PlanSkillResult }
export type { ArchitectSkillContext, ArchitectSkillResult }
export type { VerifySkillContext, VerifySkillResult }
export type { CodeReviewSkillContext, CodeReviewSkillResult }

// ---------------------------------------------------------------------------
// Utility Functions
// ---------------------------------------------------------------------------

/**
 * Get a skill by name
 */
export function getSkill(name: SkillName): EOSkill | undefined {
  return skills[name]
}

/**
 * List all registered skill names
 */
export function listSkillNames(): SkillName[] {
  return [...SKILL_NAMES]
}

/**
 * Get skill metadata
 */
export function getSkillMeta(name: SkillName) {
  return SKILL_META[name]
}

/**
 * Check if a skill name is registered
 */
export function hasSkill(name: string): name is SkillName {
  return name in skills
}
