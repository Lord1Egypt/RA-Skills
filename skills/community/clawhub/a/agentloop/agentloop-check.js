#!/usr/bin/env node
/**
 * AgentLoop Check — OpenClaw tool script
 * Sends conversation context to AgentLoop and returns a product mention if relevant.
 *
 * Usage: node agentloop-check.js <conversation> <agentResponse> [userId]
 * Requires: AGENTLOOP_API_KEY environment variable.
 * Endpoint is always https://agentloop.life — not configurable to prevent redirection.
 */

const https = require('https')
const crypto = require('crypto')

const API_KEY = process.env.AGENTLOOP_API_KEY

if (!API_KEY) {
  process.stdout.write(JSON.stringify({ shouldMention: false, error: 'AGENTLOOP_API_KEY not set. Get your key at https://agentloop.life/dashboard/api-keys' }))
  process.exit(0)
}

const [,, conversation, agentResponse, rawUserId] = process.argv

if (!conversation || !agentResponse) {
  process.stdout.write(JSON.stringify({ shouldMention: false, error: 'Missing arguments' }))
  process.exit(0)
}

// Pattern-based redaction for structured PII (emails, phones, keys, cards).
// NOTE: this does not detect free-form sensitive text (names, medical/legal content).
// The SKILL.md instructs the agent not to pass sensitive conversations to this skill.
// If your agent handles sensitive topics, add your own redaction before calling this script.
function redactStructuredPII(text) {
  return text
    .replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '[REDACTED_EMAIL]')
    .replace(/\b(?:\+?[\d\s\-().]{7,15})\b/g, (m) => /\d{7,}/.test(m) ? '[REDACTED_PHONE]' : m)
    .replace(/\b(?:sk|pk|al|key|token|secret|password|passwd|pwd)[-_]?[a-zA-Z0-9]{8,}\b/gi, '[REDACTED_KEY]')
    .replace(/\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g, '[REDACTED_CARD]')
}

// Full SHA-256 hash of userId — never truncated, never the raw value
const userId = rawUserId
  ? crypto.createHash('sha256').update(rawUserId).digest('hex')
  : crypto.randomBytes(16).toString('hex')

const body = JSON.stringify({
  conversationContext: redactStructuredPII(conversation),
  agentResponse: redactStructuredPII(agentResponse),
  userId,
})

// Endpoint is hardcoded — never redirect conversation data to a third party
const options = {
  hostname: 'agentloop.life',
  path: '/api/sdk/check',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY,
    'Content-Length': Buffer.byteLength(body),
  },
  timeout: 2500,
}

const req = https.request(options, (res) => {
  let data = ''
  res.on('data', chunk => { data += chunk })
  res.on('end', () => {
    try {
      process.stdout.write(JSON.stringify(JSON.parse(data)))
    } catch {
      process.stdout.write(JSON.stringify({ shouldMention: false }))
    }
    process.exit(0)
  })
})

req.on('error', () => {
  process.stdout.write(JSON.stringify({ shouldMention: false }))
  process.exit(0)
})

req.on('timeout', () => {
  req.destroy()
  process.stdout.write(JSON.stringify({ shouldMention: false }))
  process.exit(0)
})

req.write(body)
req.end()
