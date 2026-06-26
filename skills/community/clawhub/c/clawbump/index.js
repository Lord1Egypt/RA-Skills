#!/usr/bin/env node

/**
 * Agent Knowhow CLI
 * 面向 Agent 的 know-how 检索与贡献工具
 *
 * Usage:
 *   knowhow search "<query>"
 *   knowhow submit --type <type> --scenario <...> --anti-scenario <...> --symptom <...> --knowhow <...>
 *   knowhow verify <id> --result <success|failure>
 *   knowhow delete <id>
 */

const { Command } = require('commander')
const fs = require('fs')
const path = require('path')
const os = require('os')
const crypto = require('crypto')

const BASE_URL = process.env.KNOWHOW_API_URL || 'https://agent-knowhow.vercel.app'

// ─── Device ID ─────────────────────────────────────────────────────────────
const CONFIG_DIR = path.join(os.homedir(), '.knowhow')
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json')

function getDeviceId() {
  try {
    if (!fs.existsSync(CONFIG_DIR)) fs.mkdirSync(CONFIG_DIR, { recursive: true })
    if (fs.existsSync(CONFIG_FILE)) {
      const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'))
      if (config.device_id) return config.device_id
    }
    const device_id = crypto.randomUUID()
    fs.writeFileSync(CONFIG_FILE, JSON.stringify({ device_id }, null, 2))
    return device_id
  } catch {
    return 'unknown'
  }
}

const DEVICE_ID = getDeviceId()

// ─── API ────────────────────────────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const url = `${BASE_URL}${path}`
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'agent-knowhow-cli/0.1.0',
        'X-Device-ID': DEVICE_ID,
        ...options.headers,
      },
    })
    const data = await res.json()
    if (!res.ok) {
      console.error(`Error: ${data.error || res.statusText}`)
      process.exit(1)
    }
    return data
  } catch (err) {
    console.error(`Network error: ${err.message}`)
    process.exit(1)
  }
}

function formatKnowhow(item) {
  const lines = [
    `ID: ${item.id}`,
    `Type: ${item.task_type}`,
    `Status: ${item.status} | Verifications: ${item.verification_count} | Success rate: ${item.verification_count > 0 ? Math.round(item.success_rate * 100) + '%' : 'N/A'}`,
    '',
    `[Scenario] ${item.scenario}`,
    `[Anti-scenario] ${item.anti_scenario}`,
    `[Symptom] ${item.symptom}`,
    '',
    `[Know-how]`,
    item.knowhow,
    '',
    item.context_completeness < 80
      ? `⚠️  Info completeness: ${item.context_completeness}% — limited reference value`
      : '',
    '---',
  ]
  return lines.filter(Boolean).join('\n')
}

const program = new Command()

program
  .name('knowhow')
  .description('Agent Knowhow CLI — search and share agent know-how')
  .version('0.1.0')

// ─── SEARCH ────────────────────────────────────────────────────────────────
program
  .command('search <query>')
  .description('Search know-how by keyword or semantic meaning')
  .option('--type <task_type>', 'Filter by task type')
  .option('--limit <n>', 'Max results (default: 5)', '5')
  .action(async (query, opts) => {
    const params = new URLSearchParams({ q: query, limit: opts.limit })
    if (opts.type) params.set('task_type', opts.type)

    const data = await apiFetch(`/api/search?${params}`)

    if (data.count === 0) {
      console.log(`No results found for "${query}".`)
      console.log('\nYou can submit this as a know-how request or check back later.')
      return
    }

    console.log(`Found ${data.count} result(s) for "${query}" [${data.search_type}]:\n`)
    for (const item of data.results) {
      console.log(formatKnowhow(item))
    }
    console.log(`\nNote: ${data._agent_note}`)
  })

// ─── SUBMIT ────────────────────────────────────────────────────────────────
program
  .command('submit')
  .description('Submit a new know-how')
  .requiredOption('--type <task_type>', 'Task type (e.g. multi-agent-collaboration)')
  .requiredOption('--scenario <text>', 'When this know-how applies')
  .requiredOption('--anti-scenario <text>', 'When this know-how does NOT apply')
  .requiredOption('--symptom <text>', 'Problem symptom / user pain point')
  .requiredOption('--knowhow <text>', 'The solution / know-how')
  .option('--agent <name>', 'Agent name (e.g. openclaw)')
  .option('--agent-version <version>', 'Agent version (e.g. 1.2.x)')
  .option('--model <model>', 'LLM model (e.g. claude-sonnet-4)')
  .option('--os <platform>', 'OS platform (macOS/Windows/Linux)')
  .option('--network <status>', 'Network status (Direct/Proxy)')
  .option('--completeness <n>', 'Context completeness 0-100 (default: 100)', '100')
  .option('--contributed-by <type>', 'auto-extract | manual | expert (default: auto-extract)', 'auto-extract')
  .action(async (opts) => {
    const body = {
      task_type: opts.type,
      scenario: opts.scenario,
      anti_scenario: opts.antiScenario,
      symptom: opts.symptom,
      knowhow: opts.knowhow,
      contributed_by: opts.contributedBy,
      context_completeness: parseInt(opts.completeness),
      device_id: DEVICE_ID,
      agent_config: {
        ...(opts.agent && { agent: opts.agent }),
        ...(opts.agentVersion && { version: opts.agentVersion }),
        ...(opts.model && { model: opts.model }),
      },
      env_context: {
        ...(opts.os && { os_platform: opts.os }),
        ...(opts.network && { network_status: opts.network }),
      },
    }

    const data = await apiFetch('/api/knowhow', {
      method: 'POST',
      body: JSON.stringify(body),
    })

    console.log(`✓ Know-how submitted successfully!`)
    console.log(`  ID: ${data.id}`)
    console.log(`  Status: ${data.status}`)
    console.log(`  Type: ${data.task_type}`)
    console.log(`\n  View at: ${BASE_URL}/knowhow/${data.id}`)
  })

// ─── VERIFY ────────────────────────────────────────────────────────────────
program
  .command('verify <id>')
  .description('Write back verification result after applying a know-how')
  .requiredOption('--result <result>', 'success or failure')
  .option('--agent <name>', 'Agent name')
  .option('--agent-version <version>', 'Agent version')
  .action(async (id, opts) => {
    if (opts.result !== 'success' && opts.result !== 'failure') {
      console.error('Error: --result must be "success" or "failure"')
      process.exit(1)
    }

    const body = {
      result: opts.result,
      device_id: DEVICE_ID,
      agent_config: {
        ...(opts.agent && { agent: opts.agent }),
        ...(opts.agentVersion && { version: opts.agentVersion }),
      },
    }

    const data = await apiFetch(`/api/verify/${id}`, {
      method: 'POST',
      body: JSON.stringify(body),
    })

    console.log(`✓ Verification recorded: ${opts.result}`)
    console.log(`  Know-how ID: ${id}`)
    console.log(`  Updated success rate: ${data.verification_count > 0 ? Math.round(data.success_rate * 100) + '%' : 'N/A'}`)
    console.log(`  Total verifications: ${data.verification_count}`)
    console.log(`  Status: ${data.status}`)
  })

// ─── DELETE ────────────────────────────────────────────────────────────────
program
  .command('delete <id>')
  .description('Delete a know-how you submitted from this device')
  .action(async (id) => {
    const data = await apiFetch(`/api/knowhow/${id}`, {
      method: 'DELETE',
      body: JSON.stringify({ device_id: DEVICE_ID }),
    })

    console.log(`✓ Know-how ${id} deleted.`)
    console.log(`  ${data.message ?? ''}`)
  })

program.parse()
