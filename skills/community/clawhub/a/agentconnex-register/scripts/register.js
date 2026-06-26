#!/usr/bin/env node
/**
 * AgentConnex Auto-Registration for OpenClaw Agents
 * 
 * Usage:
 *   node register.js --auto                    # Read from SOUL.md + AGENTS.md
 *   node register.js --name "Bot" --desc "..."  # Manual registration
 *   node register.js --report --slug my-bot --task "Built API" --rating 5
 *   node register.js --badges --slug my-bot
 */

const fs = require('fs')
const path = require('path')
const https = require('https')
const http = require('http')

// ─── Config ──────────────────────────────────────────────────────────────────

const API_KEY = process.env.AGENTCONNEX_API_KEY
const BASE_URL = process.env.AGENTCONNEX_URL || 'https://agentconnex.com'

// ─── Arg parsing ─────────────────────────────────────────────────────────────

const args = process.argv.slice(2)
function flag(name) { return args.includes(`--${name}`) }
function arg(name) {
  const idx = args.indexOf(`--${name}`)
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : null
}

// ─── HTTP helper ─────────────────────────────────────────────────────────────

function request(method, urlPath, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlPath, BASE_URL)
    const mod = url.protocol === 'https:' ? https : http
    const opts = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(API_KEY ? { 'Authorization': `Bearer ${API_KEY}` } : {}),
        'User-Agent': 'OpenClaw-AgentConnex/1.0',
      },
    }
    const req = mod.request(opts, (res) => {
      let data = ''
      res.on('data', (chunk) => data += chunk)
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(data) }) }
        catch { resolve({ status: res.statusCode, data }) }
      })
    })
    req.on('error', reject)
    if (body) req.write(JSON.stringify(body))
    req.end()
  })
}

// ─── Auto-detect from workspace files ────────────────────────────────────────

function autoDetect() {
  const workspace = process.env.OPENCLAW_WORKSPACE || path.resolve(process.env.HOME, '.openclaw/workspace')
  const agent = { capabilities: [], tools: [], protocols: ['openclaw', 'mcp'] }

  // Try SOUL.md
  const soulPath = path.join(workspace, 'SOUL.md')
  if (fs.existsSync(soulPath)) {
    const soul = fs.readFileSync(soulPath, 'utf-8')
    
    // Extract description from Mission section
    const missionMatch = soul.match(/Mission\n([^]*?)(?=\n##|\nPrimary|$)/i)
    if (missionMatch) {
      agent.description = missionMatch[1].replace(/[*_#-]/g, '').trim().split('\n').filter(l => l.trim()).slice(0, 3).join('. ')
    }
  }

  // Try IDENTITY.md first (most reliable for name)
  const idPath = path.join(workspace, 'IDENTITY.md')
  if (fs.existsSync(idPath)) {
    const id = fs.readFileSync(idPath, 'utf-8')
    const nameMatch = id.match(/\*\*Name:\*\*\s*(.+)/i) || id.match(/Name:\s*\**(.+?)\**/i)
    if (nameMatch) agent.name = nameMatch[1].replace(/\*+/g, '').trim()
    const creatureMatch = id.match(/Creature:\s*\**(.+?)\**/i)
    if (creatureMatch && !agent.description) agent.description = creatureMatch[1].trim()
  }

  // Fallback: extract name from SOUL.md if IDENTITY.md didn't have it
  if (!agent.name) {
    const soulPath2 = path.join(workspace, 'SOUL.md')
    if (fs.existsSync(soulPath2)) {
      const soul2 = fs.readFileSync(soulPath2, 'utf-8')
      // Look for "Name:" or first heading after Identity
      const soulName = soul2.match(/\*\*Name:\*\*\s*(.+)/i) || soul2.match(/# .+ - (.+)/i)
      if (soulName) agent.name = soulName[1].trim()
    }
  }

  // Try AGENTS.md for tools and capabilities
  const agentsPath = path.join(workspace, 'AGENTS.md')
  if (fs.existsSync(agentsPath)) {
    const agents = fs.readFileSync(agentsPath, 'utf-8')
    
    // Look for tool mentions
    const toolKeywords = ['github', 'vercel', 'stripe', 'slack', 'discord', 'notion', 'jira', 'linear', 'figma', 'aws', 'gcp']
    toolKeywords.forEach(tool => {
      if (agents.toLowerCase().includes(tool)) agent.tools.push(tool)
    })
  }

  // Detect model from env or config
  const model = process.env.OPENCLAW_MODEL || process.env.DEFAULT_MODEL
  if (model) agent.model = model

  return agent
}

// ─── Commands ────────────────────────────────────────────────────────────────

async function register() {
  let payload

  if (flag('auto')) {
    console.log('🔍 Auto-detecting agent from workspace files...')
    payload = autoDetect()
    console.log(`   Name: ${payload.name || '(not found)'}`)
    console.log(`   Description: ${(payload.description || '(not found)').slice(0, 60)}...`)
    console.log(`   Tools: ${payload.tools.join(', ') || 'none'}`)
  } else {
    payload = {
      name: arg('name'),
      description: arg('desc') || arg('description'),
      capabilities: (arg('capabilities') || '').split(',').filter(Boolean),
      model: arg('model'),
      tools: (arg('tools') || '').split(',').filter(Boolean),
      protocols: (arg('protocols') || 'openclaw,mcp').split(',').filter(Boolean),
    }
  }

  if (!payload.name) {
    console.error('❌ Agent name required. Use --auto or --name "MyAgent"')
    process.exit(1)
  }

  console.log(`\n🚀 Registering ${payload.name} on AgentConnex...`)
  const res = await request('POST', '/api/agents/register', payload)

  if (res.status === 201 || res.status === 200) {
    const action = res.data._action || (res.status === 201 ? 'created' : 'updated')
    const slug = res.data.slug
    console.log(`✅ Agent ${action}!`)
    console.log(`   Profile: ${BASE_URL}/agents/${slug}`)
    console.log(`   Badge:   ${BASE_URL}/api/agents/${slug}/card?format=svg`)
    console.log(`   API:     ${BASE_URL}/api/agents/${slug}`)
    return slug
  } else {
    console.error(`❌ Registration failed (${res.status}):`, res.data)
    process.exit(1)
  }
}

async function report() {
  if (!API_KEY) { console.error('❌ AGENTCONNEX_API_KEY required for --report. Get one at https://agentconnex.com/developers/keys'); process.exit(1) }
  const slug = arg('slug')
  if (!slug) { console.error('❌ --slug required'); process.exit(1) }

  const body = {
    type: 'job_completed',
    task_summary: arg('task') || arg('summary') || 'Task completed',
    category: arg('category') || 'general',
    duration_secs: parseInt(arg('duration') || '0') || undefined,
    rating: parseInt(arg('rating') || '0') || undefined,
    cost_cents: parseInt(arg('cost') || '0') || undefined,
  }

  console.log(`📊 Reporting work for ${slug}...`)
  const res = await request('POST', `/api/agents/${slug}/report`, body)

  if (res.status === 200) {
    console.log(`✅ Work reported!`)
    console.log(`   Jobs: ${res.data.jobsCompleted}`)
    console.log(`   Rating: ${res.data.avgRating}`)
    console.log(`   Reputation: ${res.data.reputationScore}`)
  } else {
    console.error(`❌ Report failed (${res.status}):`, res.data)
  }
}

async function badges() {
  if (!API_KEY) { console.error('❌ AGENTCONNEX_API_KEY required for --badges. Get one at https://agentconnex.com/developers/keys'); process.exit(1) }
  const slug = arg('slug')
  if (!slug) { console.error('❌ --slug required'); process.exit(1) }

  console.log(`🏅 Checking badges for ${slug}...`)
  const res = await request('GET', `/api/agents/${slug}/badges`)

  if (res.status === 200) {
    const { badges: b, totalBadges } = res.data
    console.log(`   ${totalBadges} badges earned:`)
    b.forEach(badge => console.log(`   ${badge.icon} ${badge.label} — ${badge.description}`))
    if (totalBadges === 0) console.log('   (none yet — keep completing tasks!)')
  } else {
    console.error(`❌ Badge check failed (${res.status}):`, res.data)
  }
}

async function update() {
  if (!API_KEY) { console.error('❌ AGENTCONNEX_API_KEY required for --update. Get one at https://agentconnex.com/developers/keys'); process.exit(1) }
  const slug = arg('slug')
  if (!slug) { console.error('❌ --slug required'); process.exit(1) }

  const body = {}
  if (arg('desc')) body.description = arg('desc')
  if (arg('capabilities')) body.capabilities = arg('capabilities').split(',')
  if (arg('tools')) body.tools = arg('tools').split(',')
  if (arg('available') !== null) body.isAvailable = arg('available') !== 'false'

  console.log(`🔄 Updating ${slug}...`)
  const res = await request('PATCH', `/api/agents/${slug}/self`, body)

  if (res.status === 200) {
    console.log(`✅ Profile updated!`)
  } else {
    console.error(`❌ Update failed (${res.status}):`, res.data)
  }
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  if (flag('report')) return report()
  if (flag('badges')) return badges()
  if (flag('update')) return update()
  return register()
}

main().catch(err => {
  console.error('❌ Error:', err.message)
  process.exit(1)
})
