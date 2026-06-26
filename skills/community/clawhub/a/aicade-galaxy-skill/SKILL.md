---
name: aicade-galaxy-skills
description: Use this skill when the user wants to configure, export, or validate AICADE Galaxy dynamic services for AI use, including setting AICADE_GALAXY_* environment variables, using X-API-Key authentication, exporting capabilities from /admin/gateway/services, and working with responsePaths for partial JSON responses.
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

- The user wants to configure AICADE Galaxy access
- The user wants to export dynamic capabilities from `/admin/gateway/services`
- The user wants to invoke a tool from the exported artifact
- The user wants to validate or inspect the generated artifact
- The user asks how `AICADE_GALAXY_API_KEY`, `X-API-Key`, `responsePaths`, or `--args-file` work

## Required Configuration

This skill uses these environment variables in `.env`:

- `AICADE_GALAXY_BASE_URL`
- `AICADE_GALAXY_API_KEY`
- `AICADE_GALAXY_OUTPUT_PATH`

Authentication rule:

- Header name: `X-API-Key`
- Header value source: `AICADE_GALAXY_API_KEY`

## Usage

This skill has three main actions:

1. Configure `.env`
2. Export `aicade-galaxy-skill.json`
3. Invoke a tool from the exported artifact

Runtime selection rule:

- Prefer `node` first
- If `node` is unavailable, use `python3`
- If both are unavailable, tell the user to install Node.js and then rerun the skill commands

Suggested runtime checks:

```bash
node --version
python3 --version
```

### Configure Environment

If `.env` is missing or incomplete, run:

```bash
node {baseDir}/scripts/setup_env.mjs
```

Fallback when `node` is unavailable:

```bash
python3 {baseDir}/scripts/setup_env.py
```

This initializes:

- `AICADE_GALAXY_BASE_URL`
- `AICADE_GALAXY_API_KEY`
- `AICADE_GALAXY_OUTPUT_PATH`

Recommended default output directory:

- `output`

### Export Dynamic Services

To export the current dynamic services, run:

```bash
node {baseDir}/scripts/export_artifact.mjs
```

Fallback when `node` is unavailable:

```bash
python3 {baseDir}/scripts/export_artifact.py
```

The exported artifact path is:

`{AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json`

Default output directory:

`output`

### Invoke Exported Tools

Use the exported artifact together with an args file:

```bash
node {baseDir}/scripts/invoke_artifact.mjs --artifact {AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json --tool TOOL_NAME --args-file /tmp/invoke.json
```

Fallback when `node` is unavailable:

```bash
python3 {baseDir}/scripts/invoke_artifact.py --artifact {AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json --tool TOOL_NAME --args-file /tmp/invoke.json
```

The args file must contain a JSON object, for example:

```json
{
  "city": "北京",
  "responsePaths": ["reason", "error_code"]
}
```

Invoker behavior:

- Reads the artifact file and locates the target tool by `name`
- Reads request arguments from `--args-file`
- Validates required fields and field types against `inputSchema`
- Sends the request using the tool's `method`, `path`, and authentication metadata
- Returns a normalized JSON result

Normalized output shape:

- Success:
  `{"ok": true, "status": 200, "tool": "...", "serviceId": "...", "data": ..., "raw": ...}`
- Failure:
  `{"ok": false, "status": 4xx/5xx, "tool": "...", "serviceId": "...", "error": {"message": "...", "raw": ...}}`

## Examples

### Export AICADE Galaxy Services

1. Configure `.env` if needed:
   ```bash
   node {baseDir}/scripts/setup_env.mjs
   ```
2. Export services:
   ```bash
   node {baseDir}/scripts/export_artifact.mjs
   ```
3. Read `{AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json` and summarize or validate the generated tools.

If `node` is not available, use these fallback commands instead:

```bash
python3 {baseDir}/scripts/setup_env.py
python3 {baseDir}/scripts/export_artifact.py
```

### Invoke A Tool From Artifact

1. Prepare an args file:
   ```json
   {
     "city": "北京",
     "responsePaths": ["reason", "error_code"]
   }
   ```
2. Invoke the tool:
   ```bash
   node {baseDir}/scripts/invoke_artifact.mjs --artifact {AICADE_GALAXY_OUTPUT_PATH}/aicade-galaxy-skill.json --tool simple_weather --args-file /tmp/invoke.json
   ```
3. Read the normalized JSON output and summarize it for the user.

### Explain Response Selection

If the user asks how to return only part of a JSON response:

1. Explain that the skill uses `responsePaths`
2. Give examples such as:
   - `["city", "weather"]`
   - `["received.prompt"]`
3. Explain:
   - One path returns the selected value directly
   - Multiple paths return a nested JSON object containing only the selected fields

## Service Rules

- All service responses are JSON
- `GET` services use query parameters
- `POST` services use JSON request bodies
- Dynamic service discovery comes from `GET /admin/gateway/services`
- Tool invocation should use the exported artifact metadata instead of guessing request shapes

## Response Selection

Use `responsePaths` when the caller wants only part of the JSON response.

- `["city", "weather"]`
- `["received.prompt"]`
- `["result.realtime.temperature", "result.city"]`

Behavior:

- One path returns the selected value directly
- Multiple paths return a nested JSON object containing only the selected fields

## Files In This Skill

- `scripts/setup_env.mjs`: preferred interactive `.env` setup for Node hosts
- `scripts/export_artifact.mjs`: preferred artifact export for Node hosts
- `scripts/invoke_artifact.mjs`: preferred standalone artifact invoker for Node hosts
- `scripts/setup_env.py`: interactive `.env` setup
- `scripts/export_artifact.py`: export dynamic services into a reusable skill artifact
- `scripts/invoke_artifact.py`: standalone artifact invoker for Python hosts

## Important Constraints

- Prefer using the configured `.env` values rather than hardcoding endpoints or keys
- Prefer `node scripts/*.mjs` first, then fall back to `python3 scripts/*.py`
- If neither `node` nor `python3` is available, tell the user to install Node.js
- Do not ask the user to manually craft the artifact if `node scripts/export_artifact.mjs` or `python3 scripts/export_artifact.py` can generate it
- Do not ask the AI to construct raw HTTP requests when `scripts/invoke_artifact.mjs` or `scripts/invoke_artifact.py` can invoke the tool from artifact metadata
- Always pass tool arguments through `--args-file` as a JSON object
- If export fails with `401` or `403`, check `AICADE_GALAXY_API_KEY` first
