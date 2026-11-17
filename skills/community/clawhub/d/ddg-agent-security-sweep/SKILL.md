---
name: ddg-agent-security-sweep
description: >-
  Run one release-time security sweep over an agent's own surfaces: prompt-injection
  exposure, MCP tool permission boundaries, secret leaks, and dependency risk. Use
  before tagging a release, after adding a tool, or when a scanner flags your repo.
  Four paid calls per sweep, all inline, no operator queue.
version: 1.0.0
metadata:
  triggers: |-
    security sweep before release
    scan my mcp tools for risk
    prompt injection exposure check
    secret leak and dependency risk scan
  kind: workflow
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: DDG_AGENT_ID
        required: false
        description: Stable agent identity sent as X-Agent-Id; enables the metered free tier and keeps calls attributable.
    homepage: https://agents.daedalusdevelopmentgroup.com
    emoji: "🛡"
allowed-tools: Bash, Read, Write
---

# DDG Agent Security Sweep

An agent that ships tools and prompts needs a repeatable pre-release gate. This
sweep is four DDG calls, all automated and delivered inline in the paid response,
so it fits inside CI or a pre-tag checklist.

**Endpoints ($0.01/call, x402 on Base, USDC):**
`POST /v1/prompt-injection-scan`, `POST /v1/mcp-tool-security-audit`,
`POST /v1/secret-leak-api-key-scan`, plus one dependency scan
(`/v1/python-dependency-risk-scan` or `/v1/npm-dependency-risk-scan`).

**External cost:** $0.01 per call in USDC on Base via x402 (four calls
per sweep). The prompt-injection scan is free for the first 25 calls/day
per identity. No account or API key is required; the paid path needs an
x402-capable client.

**Free tier:** the first 25 calls/day per `X-Agent-Id` are free on
`/v1/prompt-injection-scan` (and the other funnel routes); the remaining calls
return a 402 whose body carries the paid amount and upgrade path. Invalid bodies
are rejected with 422 **before** any unit is consumed, so a malformed sweep costs
nothing.

## Procedure

1. **Prompt-injection exposure** — send the agent's system prompt, tool
   descriptions, or a captured hostile input:
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/prompt-injection-scan \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"content":"<prompt or tool description>"}' > out/injection.json
   ```
   Read `risk_summary` and `exploit_reproduction_steps`; treat any reproduction
   step as a release blocker.
2. **Tool boundary audit** — pass the tool list exactly as your agent exposes it:
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/mcp-tool-security-audit \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"tools":[{"name":"run_shell","description":"execute a command"}]}' > out/tools.json
   ```
   `tool_risk_matrix` flags dangerous capabilities and missing auth boundaries.
3. **Secret leak scan** — feed config, logs, or a diff:
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/secret-leak-api-key-scan \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"content":"<file or diff text>"}' > out/secrets.json
   ```
   Findings are returned **redacted**; rotate anything in `leak_paths`.
4. **Dependency risk** — one call with the manifest body:
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/npm-dependency-risk-scan \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"content":"<package.json or lockfile>"}' > out/deps.json
   ```
   (Python projects: `/v1/python-dependency-risk-scan`.)
5. **Gate the release** — fail the tag when: injection reproduction steps exist,
   `tool_risk_matrix` has an unauthenticated dangerous capability, secrets are
   found, or dependency risk is high.
6. **On 402** — use `upgrade_path.price_usd` and retry the same body with the
   x402 payment header. Keep the sweep body in the repo so the paid retry is
   byte-identical.

## Cost math

A sweep is 4 calls. Daily sweeps stay free inside the 25-call allowance; a
5-service monorepo doing 4 sweeps/day is 20 calls/day (free), 8 sweeps/day is 32
calls/day ≈ $0.07/day paid on the overflow.

## Failure handling

- `422` (`content_or_url_required`) = empty or malformed body; fix and resend —
  no free unit and no money are consumed.
- `503` = backend unavailable, no charge; retry with backoff.
- Never put real production secrets in the body: the scan redacts its findings,
  but the request still leaves your machine. Scan diffs and rotated-out values.

## Not for

- Not a replacement for a full code review or a penetration test — it is a
  fast, automated pre-release gate over four specific surfaces.
- Not for scanning third-party systems without authorisation, and not for
  runtime blocking (it is a batch check, not an inline WAF).

## Example

**Ask:** "Before I tag v2.3, check the new tool descriptions and this diff for
injection exposure, tool risk and leaked keys."

**Before:** the release ships on a green test suite; prompt-injection exposure and
a leaked staging key are found by a user two weeks later.

**After:** four calls in the pre-tag job produce a signed-off risk summary; the
injection reproduction step blocks the tag, the key is rotated before the release.

## Version

1.0.0 — initial workflow bundle: injection + MCP tool + secret leak + dependency
sweep with release gating and free-tier-aware 402 handling.
