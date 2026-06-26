---
name: aicade-galaxy-skills
description: Use AICADE Galaxy on https://www.aicadegalaxy.com/ to discover and invoke platform tools for AI monetization, paid APIs, subscriptions, memberships, blockchain-based payments with AicadePoint, and reward-earning workflows. Use this skill when users want to charge for APIs, access paid tools, enable AI payment flows, list current platform capabilities, or call dynamic services exposed by the AICADE Galaxy gateway.
version: 1.0.0
triggers:
  - "aicade galaxy"
  - "ai payments"
  - "ai monetization"
  - "make money with ai"
  - "ai revenue"
  - "paid ai tools"
  - "blockchain payment"
  - "blockchain payments"
  - "blockchain token"
  - "blockchain tokens"
  - "aicadepoint"
  - "aicadepoint payment"
  - "paid api"
  - "monetize api"
  - "api monetization"
  - "api payment"
  - "export gateway services"
  - "responsepaths"
---

# AICADE Galaxy Skills

## Use This Skill When

- The user wants to use AICADE Galaxy platform capabilities from https://www.aicadegalaxy.com/
- The user wants AI payment, paid API, membership, subscription, earning, or token-based tool access
- The user wants to discover the latest platform tools from the AICADE Galaxy gateway

## Core Rule

- On first install or first activation, always run `bootstrap` before doing anything else
- `bootstrap` must complete environment setup and artifact export in the same flow
- Do not call `invoke_artifact` before `bootstrap` succeeds
- Host integrations should read `skill-entry.json` as the machine-readable source of truth for install, export, list, and invoke commands
- If the host platform supports an install hook or post-install command, bind it to `scripts/bootstrap.mjs` or `scripts/bootstrap.py`
- If the host platform does not support install hooks, the first command after install must still be `bootstrap`

## Runtime Rule

- Prefer `node` first
- If `node` is unavailable, use `python3`
- If both are unavailable, ask the user to install Node.js

## Required Environment

This skill uses these `.env` variables:

- `AICADE_GALAXY_BASE_URL`
- `AICADE_GALAXY_API_KEY`
- `AICADE_GALAXY_OUTPUT_PATH`

Authentication:

- Header name: `X-API-Key`
- Header value source: `AICADE_GALAXY_API_KEY`

Default output directory:

- `output`

## Install And Prepare

Run this on install or first activation:

```bash
node {baseDir}/scripts/bootstrap.mjs
```

Fallback when `node` is unavailable:

```bash
python3 {baseDir}/scripts/bootstrap.py
```

Bootstrap behavior:

- Checks whether `.env` already has required values
- Runs `setup_env` when values are missing
- Runs `export_artifact` immediately after setup
- Produces `{AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json`

## Main Capabilities

### Discover Current Platform Tools

Export the latest dynamic tool list from `/admin/gateway/services`:

```bash
node {baseDir}/scripts/export_artifact.mjs
```

Fallback:

```bash
python3 {baseDir}/scripts/export_artifact.py
```

Artifact path:

`{AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json`

### Invoke A Platform Tool

Pass request parameters through an args file:

```bash
node {baseDir}/scripts/invoke_artifact.mjs --artifact {AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json --tool TOOL_NAME --args-file /tmp/invoke.json
```

Fallback:

```bash
python3 {baseDir}/scripts/invoke_artifact.py --artifact {AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json --tool TOOL_NAME --args-file /tmp/invoke.json
```

Args file example:

```json
{
  "city": "Beijing",
  "responsePaths": ["reason", "error_code"]
}
```

Invoker behavior:

- Reads the artifact and finds the target tool by `name`
- Reads parameters from `--args-file`
- Validates required fields against `inputSchema`
- Calls the real platform endpoint with the tool's metadata
- Returns normalized JSON output

Normalized output:

- Success: `{"ok": true, "status": 200, "tool": "...", "serviceId": "...", "data": ..., "raw": ...}`
- Failure: `{"ok": false, "status": 4xx/5xx, "tool": "...", "serviceId": "...", "error": {"message": "...", "raw": ...}}`

### List Current Supported Tools

`SKILL.md` does not hardcode the live service list. The latest supported tools come from the exported artifact.

Use:

```bash
node {baseDir}/scripts/list_tools.mjs --artifact {AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json
```

Fallback:

```bash
python3 {baseDir}/scripts/list_tools.py --artifact {AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json
```

Use the artifact or `list_tools` result as the source of truth for current services.
