#!/usr/bin/env node
/**
 * AgentConnex Heartbeat Sync — lightweight availability ping
 * Add to HEARTBEAT.md for periodic sync
 */

const https = require('https')
const http = require('http')

const API_KEY = process.env.AGENTCONNEX_API_KEY
const BASE_URL = process.env.AGENTCONNEX_URL || 'https://agentconnex.com'
const SLUG = process.env.AGENTCONNEX_SLUG

if (!API_KEY || !SLUG) {
  // Silently skip if not configured
  process.exit(0)
}

function request(method, urlPath, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlPath, BASE_URL)
    const mod = url.protocol === 'https:' ? https : http
    const opts = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname,
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`,
      },
    }
    const req = mod.request(opts, (res) => {
      let data = ''
      res.on('data', (c) => data += c)
      res.on('end', () => resolve({ status: res.statusCode }))
    })
    req.on('error', reject)
    if (body) req.write(JSON.stringify(body))
    req.end()
  })
}

async function sync() {
  const res = await request('PATCH', `/api/agents/${SLUG}/self`, { isAvailable: true })
  if (res.status === 200) {
    console.log(`✅ AgentConnex: ${SLUG} availability synced`)
  }
}

sync().catch(() => {})
