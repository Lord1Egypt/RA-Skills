/**
 * cc-soul — Notification layer
 *
 * Pure logging + optional webhook. No platform binding.
 * cc-soul is a plain HTTP API — callers handle their own messaging.
 */

import { soulConfig } from './persistence.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// WEBHOOK (optional) — POST events to external URL if configured
// ═══════════════════════════════════════════════════════════════════════════════

async function postWebhook(type: string, message: string) {
  const url = soulConfig.notify_webhook
  if (!url) return
  try {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, message, ts: Date.now() }),
    })
  } catch (e: any) {
    console.error(`[cc-soul][webhook] ${e.message}`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// GROUP NOTIFICATION — log + optional webhook
// ═══════════════════════════════════════════════════════════════════════════════

export async function notifySoulActivity(message: string) {
  // Block system detection alerts (not user content)
  if (message.includes('检测到') && message.includes('进程') && (message.includes('并发运行') || message.includes('实例'))) {
    return
  }
  console.log(`[cc-soul][notify] ${message}`)
  postWebhook('activity', message)
}

// ═══════════════════════════════════════════════════════════════════════════════
// OWNER NOTIFICATION — log + optional webhook
// ═══════════════════════════════════════════════════════════════════════════════

export async function notifyOwnerDM(message: string) {
  // Block system detection alerts (not user content)
  if (message.includes('检测到') && message.includes('进程') && (message.includes('并发运行') || message.includes('实例'))) {
    return
  }
  console.log(`[cc-soul][owner] ${message}`)
  postWebhook('owner', message)
}

/**
 * Send a raw message — log only, no formatting.
 */
export async function sendRawDM(message: string) {
  console.log(`[cc-soul][raw] ${message}`)
  postWebhook('raw', message)
}

// ═══════════════════════════════════════════════════════════════════════════════
// REPLY — log only. In API mode, results are returned in HTTP response.
// In plugin mode, OpenClaw host handles messaging via its own SDK.
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Reply to a user/group. As a pure HTTP API, this only logs.
 * Callers should use the API response to deliver messages.
 */
export async function replySender(to: string, text: string, _cfg?: any) {
  console.log(`[cc-soul][reply] → ${to}: ${text.slice(0, 120)}`)
  postWebhook('reply', text)
}
