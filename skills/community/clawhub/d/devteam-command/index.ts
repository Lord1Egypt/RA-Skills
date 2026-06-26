/**
 * DevTeam Command - Reusable Pipeline
 * 
 * Spawn Dev Team anytime for any coding task
 * 
 * Usage:
 *   await spawnDevTeam('Fix UI rendering issue')
 */

interface DevTeamAgent {
  label: string
  task: string
  model: string
  timeout: number
}

const MODELS = {
  planner: 'bailian/qwen3-coder-plus',
  pm: 'bailian/qwen3.5-plus',
  coder: 'bailian/qwen3-coder-plus',
  tester: 'bailian/qwen3.5-plus',
  fixer: 'bailian/qwen3-coder-plus',
  reporter: 'bailian/kimi-k2.5',
}

const TIMEOUTS = {
  planner: 600000,
  pm: 900000,
  coder: 3600000,
  tester: 1200000,
  fixer: 1800000,
  reporter: 600000,
}

/**
 * Spawn single agent
 */
async function spawnAgent(agent: DevTeamAgent) {
  console.log(`🤖 Spawning ${agent.label}...`)
  
  const result = await sessions_spawn({
    label: agent.label,
    task: agent.task,
    model: agent.model,
    mode: 'run',
    runtime: 'subagent',
  })
  
  console.log(`✅ ${agent.label} spawned: ${result.childSessionKey}`)
  return result
}

/**
 * Wait for agent completion
 */
async function waitForAgent(label: string, timeout: number) {
  console.log(`⏳ Waiting for ${label}...`)
  
  const startTime = Date.now()
  
  while (Date.now() - startTime < timeout) {
    const status = await subagents({
      action: 'list',
      recentMinutes: 60,
    })
    
    const agent = status.recent?.find((a: any) => 
      a.label === label && a.status === 'done'
    )
    
    if (agent) {
      console.log(`✅ ${label} completed`)
      return agent
    }
    
    const failed = status.recent?.find((a: any) => 
      a.label === label && a.status === 'failed'
    )
    
    if (failed) {
      throw new Error(`${label} failed`)
    }
    
    await new Promise(resolve => setTimeout(resolve, 30000))
  }
  
  throw new Error(`${label} timeout`)
}

/**
 * Main function: Spawn full Dev Team pipeline
 */
export async function spawnDevTeam(taskDescription: string) {
  console.log('🚀 Starting Dev Team Pipeline...')
  console.log(`📝 Task: ${taskDescription}`)
  
  try {
    // Step 1: Planner
    await spawnAgent({
      label: 'planner',
      task: `Phân tích và tạo PLAN.md cho: ${taskDescription}`,
      model: MODELS.planner,
      timeout: TIMEOUTS.planner,
    })
    await waitForAgent('planner', TIMEOUTS.planner)
    
    // Step 2: PM
    await spawnAgent({
      label: 'pm',
      task: 'Đọc PLAN.md và tạo TASKS.md',
      model: MODELS.pm,
      timeout: TIMEOUTS.pm,
    })
    await waitForAgent('pm', TIMEOUTS.pm)
    
    // Step 3: Coder
    await spawnAgent({
      label: 'coder',
      task: 'Implement code theo TASKS.md',
      model: MODELS.coder,
      timeout: TIMEOUTS.coder,
    })
    await waitForAgent('coder', TIMEOUTS.coder)
    
    // Step 4: Tester
    await spawnAgent({
      label: 'tester',
      task: 'Test implementation và tạo BUGS.md',
      model: MODELS.tester,
      timeout: TIMEOUTS.tester,
    })
    await waitForAgent('tester', TIMEOUTS.tester)
    
    // Step 5: Fixer (if bugs found)
    const bugs = await getAgentOutput('tester', 'BUGS.md')
    if (bugs && bugs.length > 0) {
      await spawnAgent({
        label: 'fixer',
        task: 'Fix bugs từ BUGS.md',
        model: MODELS.fixer,
        timeout: TIMEOUTS.fixer,
      })
      await waitForAgent('fixer', TIMEOUTS.fixer)
    }
    
    // Step 6: Reporter
    await spawnAgent({
      label: 'reporter',
      task: 'Tạo RELEASE.md',
      model: MODELS.reporter,
      timeout: TIMEOUTS.reporter,
    })
    await waitForAgent('reporter', TIMEOUTS.reporter)
    
    console.log('🎉 Dev Team Pipeline Complete!')
    console.log('📁 Check docs/ for: PLAN.md, TASKS.md, BUGS.md, RELEASE.md')
    
    return {
      success: true,
      task: taskDescription,
      pipeline: 'complete',
    }
    
  } catch (error) {
    console.error('❌ Dev Team Pipeline Failed:', error)
    return {
      success: false,
      error: error.message,
    }
  }
}

/**
 * Get agent output
 */
async function getAgentOutput(label: string, filename: string) {
  console.log(`📄 Getting ${filename} from ${label}...`)
  return null
}

/**
 * Spawn planner only
 */
export async function spawnPlanner(task: string) {
  return spawnAgent({
    label: 'planner',
    task: task,
    model: MODELS.planner,
    timeout: TIMEOUTS.planner,
  })
}

/**
 * Spawn coder only
 */
export async function spawnCoder(task: string) {
  return spawnAgent({
    label: 'coder',
    task: task,
    model: MODELS.coder,
    timeout: TIMEOUTS.coder,
  })
}

/**
 * Spawn tester only
 */
export async function spawnTester(task: string) {
  return spawnAgent({
    label: 'tester',
    task: task,
    model: MODELS.tester,
    timeout: TIMEOUTS.tester,
  })
}

// Export
export default {
  spawnDevTeam,
  spawnPlanner,
  spawnCoder,
  spawnTester,
}
