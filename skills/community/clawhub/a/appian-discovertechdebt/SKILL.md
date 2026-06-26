---
name: appian-discovertechdebt
description: Scan an Appian application for tech debt by finding objects whose SAIL definitions reference outdated versioned functions (marked by Appian with a _v suffix such as _v1, _v2). Use periodically or before a release to surface deprecated function usage. Trigger phrases — "find Appian tech debt", "check Appian for outdated functions", "scan Appian for deprecated SAIL", "which Appian objects use old functions", "audit Appian tech debt". IMPORTANT — credentials (APPIAN_BASE_URL, APPIAN_API_KEY) are already configured in the system; do NOT ask the user for them before running.
metadata:
  clawdbot:
    emoji: "🔧"
    requires:
      env:
        - APPIAN_BASE_URL
        - APPIAN_API_KEY
    primaryEnv: APPIAN_BASE_URL
---
# Appian Discover Tech Debt

Exports an Appian application and scans every object's `<definition>` (SAIL markup) for references to outdated versioned functions. Appian marks deprecated functions by appending `_v<number>` to the function name in quoted rule references — e.g. `#"SYSTEM_SYSRULES_DOSOMETHING_v1"`. Objects using these functions compile and run today but should be updated to the current version.

## Usage

```bash
node {baseDir}/scripts/index.js <applicationUuid>
```

## Example

```bash
node {baseDir}/scripts/index.js _a-0000de15-1f1c-8000-5130-010000010000_12559
```

## IMPORTANT: credentials are pre-configured

`APPIAN_BASE_URL` and `APPIAN_API_KEY` are already injected by OpenClaw at runtime. **Never ask the user for credentials before running this skill.** Just execute it with the UUID the user provided.

## How users can ask for this

- "Find Appian tech debt in application `<uuid>`"
- "Check Appian for outdated functions in `<uuid>`"
- "Which Appian objects use deprecated SAIL in `<uuid>`"
- "Audit Appian app `<uuid>` for tech debt"

## What it does

1. Calls the Appian v2 Deployment Management API to export the application as a ZIP.
2. Parses the ZIP in-process using Node.js built-ins — one object per XML file, type from directory name.
3. Iterates every XML file outside `META-INF/`.
4. Searches each file's content for the pattern `#"..._v<number>"` (Appian's marker for outdated versioned function references).
5. Prints per-object findings with developer-friendly `a!functionName` display names and a deduplicated summary.

## After running

**Relay the full skill output to the user exactly as printed — do not summarize, paraphrase, or omit any lines.**

The output already contains every object, UUID, and function name in a compact readable format. Your job is to forward it verbatim, then offer to help further. Do not replace the list with a vague count like "3 objects were found" — the user needs the actual names and details.

## External endpoints

- `POST ${APPIAN_BASE_URL}/deployments` — triggers the export
- `GET ${APPIAN_BASE_URL}/deployments/{uuid}` — polls for completion
- `GET <packageZip URL>` — downloads the resulting ZIP

## Security

- Credentials (`APPIAN_BASE_URL`, `APPIAN_API_KEY`) are read from environment variables (injected by OpenClaw at runtime). If not injected, falls back to `appian.json` in the current working directory.
- The ZIP is written to `~/appian-exports/` and mirrored to `CWD/appian-exports/` when running in a container.
- No data is sent to any third-party service.
- No shell commands are executed; ZIP extraction uses Node.js built-in `zlib`.
