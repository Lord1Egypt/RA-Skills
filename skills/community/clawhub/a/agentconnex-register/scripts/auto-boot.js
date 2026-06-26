#!/usr/bin/env node
/**
 * AgentConnex Zero-Config Auto-Boot Registration
 *
 * Runs on agent boot. Registers once, then exits silently on subsequent boots.
 * No API key required. No dependencies — pure Node.js.
 *
 * Usage (add to AGENTS.md):
 *   On first session startup, run: node ~/.openclaw/workspace/skills/agentconnex-register/scripts/auto-boot.js
 */

const fs = require('fs')
const path = require('path')
const https = require('https')

const BOOT_FILE = path.join(process.env.HOME, '.config', 'agentconnex', 'boot-registered.json')
const BASE_URL = 'agentconnex.com'

// Already registered — exit silently
if (fs.existsSync(BOOT_FILE)) {
  try {
    const data = JSON.parse(fs.readFileSync(BOOT_FILE, 'utf-8'))
    if (data.registered_at || data.agent_id || data.slug || data.profile_url) process.exit(0)
  } catch {}
}

function readFile(filePath) {
  try { return fs.readFileSync(filePath, 'utf-8') } catch { return null }
}

function extractAgent() {
  const workspace = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace')
  const agent = { capabilities: [], tools: [], protocols: ['openclaw', 'mcp'] }

  const soul = readFile(path.join(workspace, 'SOUL.md'))
  if (soul) {
    const missionMatch = soul.match(/Mission\n([^]*?)(?=\n##|\nPrimary|$)/i)
    if (missionMatch) {
      agent.description = missionMatch[1].replace(/[*_#-]/g, '').trim().split('\n').filter(l => l.trim()).slice(0, 3).join('. ')
    }
  }

  const identity = readFile(path.join(workspace, 'IDENTITY.md'))
  if (identity) {
    const nameMatch = identity.match(/\*\*Name:\*\*\s*(.+)/i) || identity.match(/Name:\s*\**(.+?)\**/i)
    if (nameMatch) agent.name = nameMatch[1].replace(/\*+/g, '').trim()
    if (!agent.description) {
      const creatureMatch = identity.match(/Creature:\s*\**(.+?)\**/i)
      if (creatureMatch) agent.description = creatureMatch[1].trim()
    }
  }

  if (!agent.name && soul) {
    const soulName = soul.match(/\*\*Name:\*\*\s*(.+)/i) || soul.match(/# .+ - (.+)/i)
    if (soulName) agent.name = soulName[1].trim()
  }

  const model = process.env.OPENCLAW_MODEL || process.env.DEFAULT_MODEL
  if (model) agent.model = model

  return agent
}

function post(payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload)
    const opts = {
      hostname: BASE_URL,
      port: 443,
      path: '/api/agents/register',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'User-Agent': 'OpenClaw-AgentConnex/1.0',
      },
    }
    const req = https.request(opts, (res) => {
      let data = ''
      res.on('data', (chunk) => data += chunk)
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(data) }) }
        catch { resolve({ status: res.statusCode, data }) }
      })
    })
    req.setTimeout(8000, () => { req.destroy(); reject(new Error('timeout')) })
    req.on('error', reject)
    req.write(body)
    req.end()
  })
}

async function main() {
  const agent = extractAgent()
  if (!agent.name) return // Can't register without a name — exit silently

  const res = await post(agent)
  if (res.status !== 200 && res.status !== 201) return

  const { agent_id, slug, profile_url } = res.data || {}

  // Save registration state
  const configDir = path.join(process.env.HOME, '.config', 'agentconnex')
  fs.mkdirSync(configDir, { recursive: true })
  fs.writeFileSync(BOOT_FILE, JSON.stringify({ agent_id, slug, profile_url, registered_at: new Date().toISOString() }, null, 2))

  console.log(`[AgentConnex] Registered: ${profile_url || `https://agentconnex.com/agents/${slug}`}`)
}

main().catch(() => process.exit(0))
