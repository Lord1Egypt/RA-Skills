// ============================================================================
// EO Verify Skill - Checkpoint Verification System
// ============================================================================

import type { ExpertResult, CheckpointResult, CheckItem } from '../types/index.js'
import { EXPERTS } from '../experts/data.js'
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface VerifySkillInput {
  target: string
  type: 'code' | 'architecture' | 'test' | 'security' | 'performance' | 'accessibility'
  criteria?: string[]
  depth?: 'quick' | 'standard' | 'deep'
}

export interface VerifySkillContext {
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

export interface VerifySkillResult {
  success: boolean
  output: string
  expertResults: ExpertResult[]
  checkpointResults: CheckpointResult[]
  durationMs: number
  overallPassed: boolean
  error?: string
}

// ---------------------------------------------------------------------------
// Verification Checkpoints by Type
// ---------------------------------------------------------------------------

const VERIFICATION_CHECKPOINTS: Record<string, CheckpointDefinition[]> = {
  'code': [
    { id: 'cp-code-001', name: 'Code compiles without errors', category: 'build' },
    { id: 'cp-code-002', name: 'Unit tests pass (if present)', category: 'test' },
    { id: 'cp-code-003', name: 'No hardcoded secrets or credentials', category: 'security' },
    { id: 'cp-code-004', name: 'Error handling is present', category: 'robustness' },
    { id: 'cp-code-005', name: 'No console.log/debug statements in production code', category: 'code-quality' },
    { id: 'cp-code-006', name: 'Code follows style guidelines', category: 'code-quality' },
  ],
  'architecture': [
    { id: 'cp-arch-001', name: 'Architecture matches specification', category: 'design' },
    { id: 'cp-arch-002', name: 'Technology choices are justified', category: 'design' },
    { id: 'cp-arch-003', name: 'Modules have clear boundaries', category: 'modularity' },
    { id: 'cp-arch-004', name: 'No circular dependencies detected', category: 'modularity' },
    { id: 'cp-arch-005', name: 'Data flow is unidirectional', category: 'design' },
  ],
  'test': [
    { id: 'cp-test-001', name: 'Core business logic is tested', category: 'coverage' },
    { id: 'cp-test-002', name: 'Happy path scenarios covered', category: 'coverage' },
    { id: 'cp-test-003', name: 'Error paths have test cases', category: 'coverage' },
    { id: 'cp-test-004', name: 'Tests are deterministic', category: 'quality' },
    { id: 'cp-test-005', name: 'Test isolation is maintained', category: 'quality' },
  ],
  'security': [
    { id: 'cp-sec-001', name: 'Input validation on all endpoints', category: 'validation' },
    { id: 'cp-sec-002', name: 'Authentication is enforced', category: 'auth' },
    { id: 'cp-sec-003', name: 'Authorization follows least privilege', category: 'auth' },
    { id: 'cp-sec-004', name: 'No SQL injection vulnerabilities', category: 'injection' },
    { id: 'cp-sec-005', name: 'Sensitive data is encrypted at rest', category: 'encryption' },
    { id: 'cp-sec-006', name: 'HTTPS enforced for all communications', category: 'transport' },
    { id: 'cp-sec-007', name: 'Dependencies have no known CVEs', category: 'dependencies' },
  ],
  'performance': [
    { id: 'cp-perf-001', name: 'API response time < 200ms (p95)', category: 'latency' },
    { id: 'cp-perf-002', name: 'No N+1 query problems', category: 'database' },
    { id: 'cp-perf-003', name: 'Appropriate caching in place', category: 'caching' },
    { id: 'cp-perf-004', name: 'Connection pooling configured', category: 'database' },
    { id: 'cp-perf-005', name: 'Lazy loading used where appropriate', category: 'loading' },
  ],
  'accessibility': [
    { id: 'cp-a11y-001', name: 'All images have alt text', category: 'images' },
    { id: 'cp-a11y-002', name: 'Color contrast meets WCAG AA', category: 'visual' },
    { id: 'cp-a11y-003', name: 'Keyboard navigation works', category: 'navigation' },
    { id: 'cp-a11y-004', name: 'ARIA labels present where needed', category: 'aria' },
    { id: 'cp-a11y-005', name: 'Focus indicators are visible', category: 'navigation' },
  ],
}

interface CheckpointDefinition {
  id: string
  name: string
  category: string
}

// ---------------------------------------------------------------------------
// Verify Skill Definition
// ---------------------------------------------------------------------------

export const verifySkill = {
  name: 'verify',
  description: 'Verify implementation against specifications using checkpoint-based validation',
  expert: 'qa',
  role: 'qa',

  async execute(
    args: string,
    context: VerifySkillContext
  ): Promise<VerifySkillResult> {
    const startTime = Date.now()
    const logger = context.logger

    // 1. Parse arguments
    const input = parseVerifyInput(args)
    logger.info(`[verify-skill] Starting ${input.type} verification for: ${input.target.slice(0, 50)}...`)

    // 2. Get checkpoints for type
    const checkpoints = VERIFICATION_CHECKPOINTS[input.type] ?? VERIFICATION_CHECKPOINTS['code']
    const criteriaStr = input.criteria?.length
      ? `\n\nAdditional verification criteria:\n${input.criteria.map(c => `- ${c}`).join('\n')}`
      : ''

    // 3. Determine expert team based on type
    const expertTeamMap: Record<string, string[]> = {
      'code': ['qa-001', 'rev-001'],
      'architecture': ['rev-003', 'arch-001'],
      'test': ['qa-001', 'qa-002'],
      'security': ['sec-001', 'sec-004'],
      'performance': ['qa-003', 'rev-004'],
      'accessibility': ['fe-003', 'qa-001'],
    }
    const expertIds = expertTeamMap[input.type] ?? expertTeamMap['code']
    const experts = expertIds
      .map(id => EXPERTS[id])
      .filter((e): e is NonNullable<typeof e> => e !== undefined)

    logger.info(`[verify-skill] Expert team: ${experts.map(e => e.name).join(', ')}`)

    // 4. Build verification prompts
    const expertPrompts: Record<string, string> = {
      'qa-001': buildExpertPrompt(
        'qa-001', 'Test Engineer',
        `Verify the following ${input.type} implementation:\n\nTarget: ${input.target}${criteriaStr}\n\nCheckpoints:\n${checkpoints.map(cp => `- [ ] ${cp.name}`).join('\n')}\n\nFor each checkpoint, indicate PASS, FAIL, or WARN with a brief explanation.`,
        { type: input.type, checkpoints: checkpoints.map(c => c.id) }
      ),
      'rev-001': buildExpertPrompt(
        'rev-001', 'Code Quality Reviewer',
        `Review code quality for:\n\n${input.target}${criteriaStr}\n\nFocus on: code quality, maintainability, and adherence to best practices.`,
        {}
      ),
      'sec-001': buildExpertPrompt(
        'sec-001', 'Application Security Engineer',
        `Perform security verification for:\n\n${input.target}${criteriaStr}\n\nFocus on: OWASP Top 10, secure coding practices, and common vulnerabilities.`,
        {}
      ),
      'qa-002': buildExpertPrompt(
        'qa-002', 'Test Automation Engineer',
        `Verify test coverage and automation for:\n\n${input.target}${criteriaStr}\n\nFocus on: test quality, coverage, and automation strategy.`,
        {}
      ),
      'qa-003': buildExpertPrompt(
        'qa-003', 'Performance QA Engineer',
        `Verify performance characteristics for:\n\n${input.target}${criteriaStr}\n\nFocus on: load profiles, bottlenecks, and optimization opportunities.`,
        {}
      ),
      'rev-003': buildExpertPrompt(
        'rev-003', 'Architecture Reviewer',
        `Review architecture for:\n\n${input.target}${criteriaStr}\n\nFocus on: design fitness, scalability, and technical debt.`,
        {}
      ),
      'arch-001': buildExpertPrompt(
        'arch-001', 'System Architect',
        `Review system architecture for:\n\n${input.target}${criteriaStr}\n\nFocus on: architectural fitness, technology selection, and system design.`,
        {}
      ),
      'rev-004': buildExpertPrompt(
        'rev-004', 'Performance Reviewer',
        `Review performance aspects for:\n\n${input.target}${criteriaStr}\n\nFocus on: performance anti-patterns, bottleneck identification.`,
        {}
      ),
      'sec-004': buildExpertPrompt(
        'sec-004', 'Security Auditor',
        `Conduct security audit for:\n\n${input.target}${criteriaStr}\n\nFocus on: penetration testing, vulnerability assessment, and compliance.`,
        {}
      ),
      'fe-003': buildExpertPrompt(
        'fe-003', 'UI/UX Designer',
        `Verify accessibility for:\n\n${input.target}${criteriaStr}\n\nFocus on: WCAG compliance, keyboard navigation, and assistive technology support.`,
        {}
      ),
    }

    // 5. Run verification in parallel
    const results: ExpertResult[] = await Promise.all(
      experts.map(async (expert) => {
        const prompt = expertPrompts[expert.id] ?? buildExpertPrompt(expert.id, expert.name, input.target, {})
        const expertStart = Date.now()

        try {
          const runResult = await context.runtime.subagent.run({
            sessionKey: context.sessionId ?? `verify:${input.type}:${input.target}`,
            message: prompt,
            extraSystemPrompt: `You are ${expert.name}, a ${expert.description}. Be thorough and critical in your verification.`,
          })

          await context.runtime.subagent.waitForRun({ runId: runResult.runId, timeoutMs: 120000 })

          const { messages } = await context.runtime.subagent.getSessionMessages({
            sessionKey: context.sessionId ?? `verify:${input.type}:${input.target}`,
            limit: 5,
          })

          const lastMsg = messages[messages.length - 1] as { content?: string } | undefined
          const output = typeof lastMsg?.content === 'string' ? lastMsg.content.slice(0, 2000) : 'No output'

          return {
            expertId: expert.id,
            expertName: expert.name,
            output,
            durationMs: Date.now() - expertStart,
            success: true,
          }
        } catch (err) {
          logger.error(`[verify-skill] Expert ${expert.name} failed: ${err}`)
          return {
            expertId: expert.id,
            expertName: expert.name,
            output: '',
            durationMs: Date.now() - expertStart,
            success: false,
            error: String(err),
          }
        }
      })
    )

    // 6. Generate checkpoint results from expert outputs
    const checkpointResults = generateCheckpointResults(checkpoints, results)

    // 7. Format output
    const checkpointOutput = formatCheckpointResults(checkpointResults)
    const expertOutput = aggregateExpertResults(
      results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })),
      `verify:${input.type}`
    )

    const overallPassed = checkpointResults.every(cp => cp.passed)
    const summary = checkpointResults.reduce(
      (acc, cp) => {
        if (cp.passed) acc.passed++
        else acc.failed++
        acc.total++
        return acc
      },
      { total: 0, passed: 0, failed: 0, warnings: 0 }
    )

    const output = `## ✅ Verification Report

### Target: ${input.target}
### Type: ${input.type.toUpperCase()}
### Depth: ${input.depth ?? 'standard'}

### Summary
- **Total Checkpoints:** ${summary.total}
- **✅ Passed:** ${summary.passed}
- **❌ Failed:** ${summary.failed}

### Checkpoint Results
${checkpointOutput}

### Expert Analysis
${expertOutput}`

    return {
      success: true,
      output,
      expertResults: results,
      checkpointResults,
      durationMs: Date.now() - startTime,
      overallPassed,
    }
  },
}

// ---------------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------------

function parseVerifyInput(args: string): VerifySkillInput {
  const params: Record<string, string> = {}
  const remaining: string[] = []

  for (const part of args.split(/\s+/)) {
    const eqIdx = part.indexOf('=')
    if (eqIdx > 0) {
      params[part.slice(0, eqIdx)] = part.slice(eqIdx + 1)
    } else {
      remaining.push(part)
    }
  }

  return {
    target: params.target ?? remaining.join(' ') ?? 'Unspecified target',
    type: (params.type ?? 'code') as VerifySkillInput['type'],
    criteria: params.criteria ? params.criteria.split(',').map(s => s.trim()) : [],
    depth: params.depth as VerifySkillInput['depth'],
  }
}

function generateCheckpointResults(
  checkpoints: CheckpointDefinition[],
  results: ExpertResult[]
): CheckpointResult[] {
  // Parse expert outputs to determine pass/fail/warn for each checkpoint
  // This is a simplified heuristic-based parser
  const combinedOutput = results.map(r => r.output).join('\n').toLowerCase()

  return checkpoints.map(cp => {
    const cpLower = cp.name.toLowerCase()
    const words = cpLower.split(/\s+/)
    
    // Heuristic: if key terms from checkpoint appear with "pass" or "ok" nearby, it's likely pass
    const hasPassIndicator = /pass|ok|good|✓|✅|no (issue|problem)/.test(combinedOutput) && 
      words.some(w => combinedOutput.includes(w) && /pass|ok|good/.test(combinedOutput.slice(combinedOutput.indexOf(w), combinedOutput.indexOf(w) + 100)))
    
    // Check for explicit fail indicators
    const hasFailIndicator = /fail|fail|✗|❌|error|issue|problem|concern/.test(combinedOutput) &&
      words.some(w => combinedOutput.includes(w) && /fail|error|issue|problem/.test(combinedOutput.slice(combinedOutput.indexOf(w), combinedOutput.indexOf(w) + 100)))

    const status: CheckItem['status'] = hasFailIndicator ? 'fail' : hasPassIndicator ? 'pass' : 'warn'

    return {
      checkpoint: cp.name,
      passed: status === 'pass',
      items: [
        {
          id: cp.id,
          name: cp.name,
          status,
          message: status === 'pass' ? 'Verified as passing' : status === 'fail' ? 'Issue detected' : 'Unable to determine - requires manual review',
        },
      ],
      summary: {
        total: 1,
        passed: status === 'pass' ? 1 : 0,
        warnings: status === 'warn' ? 1 : 0,
        failed: status === 'fail' ? 1 : 0,
      },
    }
  })
}

function formatCheckpointResults(results: CheckpointResult[]): string {
  return results
    .map(cp => {
      const icon = cp.passed ? '✅' : '❌'
      const items = cp.items.map(item => {
        const itemIcon = item.status === 'pass' ? '✅' : item.status === 'fail' ? '❌' : '⚠️'
        return `  ${itemIcon} ${item.name}: ${item.message ?? ''}`
      })
      return `${icon} **${cp.checkpoint}**\n${items.join('\n')}`
    })
    .join('\n\n')
}
