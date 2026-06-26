# Aqara Open API Deployment Guide

## Overview

This skill package uses the Aqara Open Platform API to query and control Aqara/Lumi smart home devices, and to handle space and automation related requests.

The skill layout follows a **parent router + child skills** model:

- `SKILL.md`: parent router skill. It first determines how `space`, `device`, and `automation` relate, then routes into the correct child skill.
- `device/SKILL.md`: device listing, statistics, state interpretation, and control.
- `space/SKILL.md`: space listing, creation, updates, and device membership changes.
- `automation/SKILL.md`: automation capability checks, creation, updates, enable/disable, and deletion.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `AQARA_OPEN_API_TOKEN` | Yes | Aqara Open Platform Bearer token |
| `AQARA_ENDPOINT_URL` | Yes | Aqara Open API endpoint URL, for example `https://aiot-open-3rd.aqara.cn/open/api` |

## Runtime Dependencies

- `node`: used to run the `aqara` CLI

## Execution Model

All Open API requests are executed through the unified `aqara` CLI. The CLI sends requests to the single `POST $AQARA_ENDPOINT_URL` entry point, and the request body `type` field selects the operation.

Device queries follow a **cache-first** model:

1. Use `aqara devices cache refresh` to obtain the result of `GetAllDevicesWithSpaceRequest`.
2. The CLI writes only the `data` array from the response into `data/devices.json`.
3. Subsequent device queries, statistics, and state interpretation should read `data/devices.json` first, instead of repeatedly calling the API.

Automation-related requests still go through the HTTP API, but automation capability truth must follow `QueryAutomationCapabilitiesRequest`. Do not treat `data/devices.json` as an unconditional automation capability source of truth.

## Directory Layout

```text
aqara-open-api-cli/
├── SKILL.md
├── README-CLAWHUB.md
├── README.md
├── package.json
├── bin/
│   └── aqara-open-api.js
├── lib/
│   ├── cache.js
│   ├── commands.js
│   ├── config.js
│   ├── errors.js
│   ├── http.js
│   ├── output.js
│   └── traits.js
├── docs/
│   └── commands.md
├── automation/
│   └── SKILL.md
├── device/
│   └── SKILL.md
├── space/
│   └── SKILL.md
├── assets/
│   ├── automation_examples.md
│   ├── device-space-examples.md
│   └── trait-codes.md
├── references/
│   ├── automation-http-examples.md
│   ├── automation_config.md
│   └── examples.md
├── scripts/
│   └── fetch_all_devices.sh
└── data/
    └── devices.json
```

## Credential Loading

The skill package supports two ways to provide credentials.

### 1. Via `aqara config`

```bash
aqara config set-endpoint "https://aiot-open-3rd.aqara.cn/open/api"
aqara config set-token "your-token"
aqara config show
```

If `AQARA_ENDPOINT_URL` or `AQARA_OPEN_API_TOKEN` is missing in the current execution chain, the CLI falls back to `~/.aqa/config.json`.

Hard rules:

- Do not write secrets into persistent shell profiles such as `.zshrc`, `.bashrc`, or PowerShell profiles.
- Do not echo real tokens in logs, prompts, or generated files.

### 2. Export environment variables directly

```bash
export AQARA_OPEN_API_TOKEN="your-token"
export AQARA_ENDPOINT_URL="https://aiot-open-3rd.aqara.cn/open/api"

aqara devices cache refresh
```

Expected output:

```text
OK: wrote N devices to data/devices.json
```

## Routing and Example Entry Points

Prefer routing by intent into the right document, instead of trying to understand every request from a single file:

- Device or space HTTP examples: `assets/device-space-examples.md`
- Automation HTTP lifecycle examples: `references/automation-http-examples.md`
- Automation JSON structure rules: `references/automation_config.md`
- Unified example index: `references/examples.md`

## Node CLI

This package also ships a Node.js CLI suitable for npm publishing. The entry point is `bin/aqara-open-api.js`.

Common usage:

```bash
node ./bin/aqara-open-api.js help
node ./bin/aqara-open-api.js doctor --json
node ./bin/aqara-open-api.js devices cache refresh
node ./bin/aqara-open-api.js devices list --json
node ./bin/aqara-open-api.js automations list --json
```

After installing as an npm CLI, the global command name is `aqara`:

```bash
aqara help
aqara doctor --json
aqara devices list --json
aqara automations list --json
```

CLI coverage:

- `devices`: cache refresh, device listing, device inspection, trait listing, trait execution, device type catalog
- `spaces`: list, create, update, device association
- `automations`: capabilities, list, get, create, update, rename, enable, disable, delete
- `traits`: trait catalog search and filtering based on `assets/trait-codes.md`
- `doctor`: runtime, credentials, cache, and dependency checks

Publishing and full command documentation:

- npm-oriented overview: `README.md`
- full command reference: `docs/commands.md`

## Important Rules

- **Cache-first**: for device-related queries, read `data/devices.json` first. Only re-fetch when the cache is missing, corrupted, or the user explicitly requests a refresh.
- **Full scans for totals**: device totals and grouped counts must iterate the full cached array and count by `deviceId`.
- **Space is scope, not device truth**: room semantics narrow the device scope first, then resolve concrete devices.
- **Resolve before control**: `deviceId`, `endpointId`, `functionCode`, and `traitCode` used for control must come from real cached evidence.
- **Automation capabilities first**: automation creation or config updates must consult `QueryAutomationCapabilitiesRequest` for capability truth.
- **Language policy**: prefer English for explanations, analysis, and clarifications; keep request types, field names, paths, and code examples in their original English identifiers.
