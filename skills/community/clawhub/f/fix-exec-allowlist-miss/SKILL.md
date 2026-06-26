---
name: fix-exec-allowlist-miss
description: Hybrid reload mode auto-restarts for gateway/plugins changes. Config patching requires baseHash from config.get first. Minimax cron auth uses system-level tokens, not session OAuth.
---

Diagnosing exec deny:
1. Check tools.exec.security and tools.profile in config
2. If profile=coding and security=full still denied → profile baseline missing exec
3. Use gateway tool: gateway('config.patch', {raw: '{tools:{profile:"full"}}'})
4. Hot-reload applies automatically in hybrid mode; explicit restart via gateway restart if needed
5. Verify: gateway('config.get', {}) → confirm profile=full

Config patch workflow (atomic, hash-verified):
1. gateway('config.get', {}) → capture payload.hash
2. gateway('config.patch', {raw: '...', baseHash: '<hash>'})
3. Rate limit: 3 req/60s per deviceId+clientIp. Restart coalesces with 30s cooldown.

Hot-apply vs restart fields (hybrid mode):
Hot-apply (no restart): channels, agent, models, routing, hooks, cron, session, messages, tools, browser, skills, mcp, audio, talk, ui, logging, identity, bindings
Restart required: gateway.* (port, bind, auth, TLS, HTTP), discovery, plugins
gateway.reload and gateway.remote changes do NOT trigger restart.

Minimax OAuth failure (ConnectionRefused / 401):
- Cron jobs use system-level auth, not current session OAuth → isolated session
- If minimax portal token expired: gateway('update.run', {continuationMessage: '...'}) attempts re-auth on restart
- Fallback: openclaw config set models.providers.minimax-portal.apiKey '<key>'

## Workflow

Config patch protected paths:
- Cannot patch channel-specific configs (e.g., whatsapp:8801322964987)
- Raw must be object, not string — wrong: gateway('config.patch', {raw: '{...}'})  
  Right: gateway('config.patch', {raw: {channels: {...}}})
- Protected paths raise error: gateway config.patch cannot change protected config paths: <path>
