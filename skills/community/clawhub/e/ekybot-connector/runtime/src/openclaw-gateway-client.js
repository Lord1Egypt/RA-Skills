/**
 * OpenClaw Gateway Client
 *
 * Reads OPENCLAW_GATEWAY_URL (defaults to http://127.0.0.1:18789) from
 * environment to communicate with the LOCAL OpenClaw gateway on the
 * user's machine.
 *
 * This module ONLY communicates with localhost — it does NOT send any
 * data to external servers. All calls go to the local OpenClaw gateway:
 * - POST /v1/chat/completions — dispatch @mention messages to local agents
 *
 * Authentication uses OPENCLAW_GATEWAY_TOKEN (local gateway token) and
 * identifies the target agent via x-openclaw-agent-id header.
 *
 * See references/security.md for the full architecture diagram.
 */
const fetchImpl = global.fetch
  ? (...args) => global.fetch(...args)
  : (...args) => require('node-fetch')(...args);
const { resolveRelayTimeout, resolveRelayLifecyclePolicy } = require('./relay-continuity');

class OpenClawGatewayClient {
  constructor(options = {}) {
    const baseUrl =
      options.baseUrl ||
      process.env.OPENCLAW_GATEWAY_URL ||
      process.env.EKYBOT_OPENCLAW_GATEWAY_URL ||
      'http://127.0.0.1:18789';

    this.baseUrl = String(baseUrl).replace(/\/$/, '');
    this.authToken =
      options.authToken ||
      process.env.OPENCLAW_GATEWAY_TOKEN ||
      process.env.EKYBOT_OPENCLAW_GATEWAY_TOKEN ||
      process.env.EKYBOT_GATEWAY_TOKEN ||
      null;
    this.userAgent = options.userAgent || 'ekybot-companion/relay';
    const lifecycle = resolveRelayLifecyclePolicy();
    this.timeoutMs = resolveRelayTimeout(process.env.EKYBOT_COMPANION_RELAY_TIMEOUT_MS, lifecycle.failedMs);
  }

  buildHeaders(agentId, sessionKey) {
    const headers = {
      'Content-Type': 'application/json',
      'User-Agent': this.userAgent,
      'x-openclaw-agent-id': agentId,
      'x-openclaw-session-key': sessionKey,
      'ngrok-skip-browser-warning': 'true',
    };

    if (this.authToken) {
      headers.Authorization = `Bearer ${this.authToken}`;
      headers['x-workspace-api-key'] = this.authToken;
      headers['x-agent-token'] = this.authToken;
    }

    return headers;
  }

  extractMessageContent(payload) {
    if (payload?.choices?.[0]?.message?.content && typeof payload.choices[0].message.content === 'string') {
      return payload.choices[0].message.content.trim();
    }

    if (Array.isArray(payload?.output)) {
      const textChunks = payload.output
        .map((entry) => (typeof entry?.content === 'string' ? entry.content : null))
        .filter(Boolean);
      if (textChunks.length > 0) {
        return textChunks.join('\n').trim();
      }
    }

    return '';
  }

  extractSseContent(rawText) {
    const lines = String(rawText || '').split('\n').filter((line) => line.startsWith('data: '));
    const chunks = [];

    for (const line of lines) {
      const data = line.slice(6);
      if (data === '[DONE]') {
        break;
      }
      try {
        const parsed = JSON.parse(data);
        const delta = parsed?.choices?.[0]?.delta?.content;
        if (delta) {
          chunks.push(delta);
        }
      } catch (_error) {
        // Ignore malformed SSE chunks.
      }
    }

    return chunks.join('').trim();
  }

  async sendRelayPrompt({ agentId, sessionKey, prompt, model = null }) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetchImpl(`${this.baseUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: this.buildHeaders(agentId, sessionKey),
        body: JSON.stringify({
          model: model || `openclaw:${agentId}`,
          messages: [{ role: 'user', content: prompt }],
          stream: false,
        }),
        signal: controller.signal,
      });

      const rawText = await response.text();
      if (!response.ok) {
        throw new Error(`Gateway returned ${response.status}: ${rawText.slice(0, 300)}`);
      }

      let content = '';
      try {
        const payload = JSON.parse(rawText);
        content = this.extractMessageContent(payload);
      } catch (_error) {
        content = this.extractSseContent(rawText);
      }

      return {
        content,
        rawText,
      };
    } finally {
      clearTimeout(timeoutId);
    }
  }
}

module.exports = OpenClawGatewayClient;
