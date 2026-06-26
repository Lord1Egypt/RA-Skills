# AgentTrust
## Description
Security Scanner and Reputation Oracle for AI agent skills and MCP servers. Scans for malware, prompt injection, tool poisoning, and 47 other threat patterns. Returns cryptographically signed ACT/HALT receipts (JWS, draft-krausz-verification-state-01). x402-native on Base mainnet. Conforming implementation of IETF draft-krausz-verification-state-01 alongside AgentOracle.

Unique features:
- SKILL.md scanner — 40 rules, 12 categories
- MCP manifest scanner — tool poisoning, shadowing, hidden unicode, rug pull detection
- Unified trust gate — skill + MCP + endpoint reputation in one signed call
- Composed receipt — two-issuer JWS envelope (AgentTrust + AgentOracle, Phase 1 live)
- JWS-signed receipts — verifiable ACT/HALT per IETF draft-krausz-verification-state-01
- Endpoint reputation — on-chain trust score before your agent pays
- Trust badge — SVG badge for x402 providers
- MCP server — install via npx @poteshniy/agenttrust-mcp for Claude Desktop, Cursor, Windsurf

**Privacy notice:** Submitted content is sent to agenttrust.uk for analysis. Only submit content you are comfortable sharing.

**Payment notice:** Full scan endpoints require x402 USDC payments on Base. Free tiers require no wallet.

## Instructions
Always try free endpoints first. Before using any paid endpoint, ask the user for explicit confirmation and disclose the exact price.

### Free SKILL.md scan (no payment required)
POST https://agenttrust.uk/v1/scan/free
Price: FREE
Body: { "content": "<skill content, max 50 lines>" }
Returns: safety score 0-100, level (SAFE/MEDIUM/HIGH/CRITICAL), findings, v_gate (act/halt), JWS receipt
Note: Rate limited to 10 requests/hour per IP.

### Full SKILL.md scan (requires explicit user approval)
POST https://agenttrust.uk/v1/scan
Price: 0.015 USDC on Base (x402)
Body: { "content": "<full skill content>" }
Returns: safety score, all 40 findings, integrity hash, JWS receipt
Note: Results are cached — repeated scans return instantly.

### Free MCP manifest scan (no payment required)
POST https://agenttrust.uk/v1/scan/mcp/free
Price: FREE
Body: { "manifest": <MCP server manifest JSON> }
Returns: safety score, level, findings (tool poisoning, shadowing, etc.), v_gate, JWS receipt
Note: Rate limited to 10 requests/hour per IP.

### Full MCP manifest scan (requires explicit user approval)
POST https://agenttrust.uk/v1/scan/mcp
Price: 0.015 USDC on Base (x402)
Body: { "manifest": <MCP server manifest JSON> }
Returns: full scan, all 50 rules, JWS receipt

### Unified trust gate (FREE)
POST https://agenttrust.uk/v1/gate
Price: FREE
Body: { "skill": "<content>", "mcp": <manifest>, "endpoint": "<url>" }
Note: All fields optional — include whichever you want to check.
Returns: v_gate (act/halt), v_recommendation, worst_level, per-component results, JWS receipt
Use this to check everything at once before your agent acts.

### Composed receipt (FREE)
POST https://agenttrust.uk/v1/compose
Price: FREE
Body: { "claim_hash": "sha256-...", "skill": "<content>", "mcp": <manifest> }
Returns: two-issuer JWS envelope (AgentTrust + AgentOracle), composed_decision (act/halt)
Note: Phase 1 live — two signers. Phase 2 adds Presidio as third signer.

### Sign canonical bytes (FREE)
POST https://agenttrust.uk/v1/sign
Price: FREE
Body: { "canonical_bytes_b64u": "<base64url encoded bytes>" }
Returns: AT signature + protected header for composed JWS assembly

### Endpoint reputation check (FREE)
GET https://agenttrust.uk/v1/reputation?url=<endpoint_url>
Price: FREE
Returns: trust score 0-100, badge (TRUSTED/UNVERIFIED/SUSPICIOUS), issues, on-chain stats

### Trust badge (FREE)
GET https://agenttrust.uk/v1/badge?url=<endpoint_url>
Price: FREE
Returns: SVG badge — embed with <img src="https://agenttrust.uk/v1/badge?url=YOUR_ENDPOINT"/>

### Wallet reputation lookup (requires explicit user approval)
GET https://agenttrust.uk/v1/trust/:address
Price: 0.010 USDC on Base (x402)
Returns: trust score, incident history, audit status

### Verify integrity (requires explicit user approval)
POST https://agenttrust.uk/v1/verify
Price: 0.005 USDC on Base (x402)
Body: { "hash": "<sha256>" } or { "content": "<skill content>" }
Returns: verified true/false, last scan result

### Full audit report (requires explicit user approval)
POST https://agenttrust.uk/v1/report
Price: 0.050 USDC on Base (x402)
Body: { "content": "<skill content>", "skill_id": "<name>" }
Returns: full report with per-finding remediation guidance

### MCP Server (Claude Desktop / Cursor / Windsurf)
Install once and use all tools directly in your AI client:
npx @poteshniy/agenttrust-mcp

Config:
{"mcpServers":{"agenttrust":{"command":"npx","args":["-y","@poteshniy/agenttrust-mcp"]}}}

### JWS Receipt Verification
All scan responses include a signed receipt field. Verify with:
JWKS: https://agenttrust.uk/.well-known/jwks.json
Mapping: https://raw.githubusercontent.com/poteshniy/agenttrust/main/docs/mapping-v0.3.md
Spec: https://datatracker.ietf.org/doc/draft-krausz-verification-state/
