---
name: dual-memory
description: "Run memory-core AND external memory providers (like SuperMemory) together in one slot — with full dreaming support. OpenClaw only allows one memory plugin, so this composite proxy lets you keep local QMD search + MEMORY.md + dreaming (Light/REM/Deep) while also getting cloud persistence from SuperMemory or other providers. Searches merge across all backends, writes go to both."
version: 1.0.7
metadata: {"openclaw":{"primaryEnv":"SUPERMEMORY_OPENCLAW_API_KEY"}}
---

# Dual Memory Plugin

Keep **memory-core + dreaming** AND add **external memory providers** like SuperMemory — all in one memory slot. No more choosing between local and cloud.

## The Problem

OpenClaw only allows **one plugin per `kind: "memory"`**. You have to choose between:
- **memory-core** — local MEMORY.md, QMD vector search, dreaming (Light/REM/Deep consolidation)
- **External providers** like SuperMemory — cloud persistence across sessions, devices, and agents

This plugin eliminates the choice. You get **memory-core + dreaming + any external provider** in a single slot. The proxy pattern means you never lose native dreaming when adding cloud memory.

## How It Works

The plugin legitimately holds the memory slot and delegates to both backends via a proxy pattern:

```
dual-memory (holds memory slot)
├── Proxy API → memory-core (local)
│   ├── QMD vector search
│   ├── MEMORY.md management
│   └── Dreaming consolidation
└── Proxy API → supermemory (cloud)
    ├── Cloud vector search
    ├── Cross-session persistence
    └── Profile/entity context
```

- **Searches** query both backends, results are merged and deduplicated
- **Writes** go to memory-core (local MEMORY.md). SuperMemory captures conversation content automatically via auto-capture hook.
- **Dreaming** runs through memory-core's native consolidation cycle
- **Recall** injects context from both local (QMD) and cloud (SuperMemory) sources

## Install

### Via ClawdHub

```bash
npx clawhub@latest install dual-memory
```

### Manual

```bash
# Clone to extensions
cp -r dual-memory ~/.openclaw/extensions/
cd ~/.openclaw/extensions/dual-memory
npm install
```

### Dependency

This plugin requires `openclaw-supermemory` as a sibling extension:

```
~/.openclaw/extensions/
├── dual-memory/   ← this plugin
└── openclaw-supermemory/        ← required sibling
```

Install supermemory from ClawdHub: `npx clawhub@latest install supermemory`

## Configuration

Add to your OpenClaw config. **Disable the individual plugins** — the composite replaces them:

```yaml
plugins:
  entries:
    # Disable individual plugins (composite handles both)
    memory-core:
      enabled: false
    openclaw-supermemory:
      enabled: false
    # Enable composite
    dual-memory:
      enabled: true
      config:
        supermemory:
          apiKey: "${SUPERMEMORY_OPENCLAW_API_KEY}"
          containerTag: "my_agent"
          autoRecall: true
          autoCapture: true
          maxRecallResults: 5
          captureMode: "everything"
        memoryCore:
          dreaming:
            enabled: true
            frequency: "30 2 * * *"
```

### SuperMemory Options

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `apiKey` | string | env var | SuperMemory API key (supports `${ENV_VAR}`) |
| `containerTag` | string | hostname | Isolates memories per agent/machine |
| `autoRecall` | boolean | true | Auto-inject relevant memories |
| `autoCapture` | boolean | true | Auto-store important info |
| `maxRecallResults` | number | 5 | Max memories per conversation (1-20) |
| `captureMode` | string | everything | Capture mode |
| `profileFrequency` | number | — | Profile refresh interval (1-500) |
| `debug` | boolean | false | Verbose logging |
| `enableCustomContainerTags` | boolean | false | Allow multiple containers |
| `customContainers` | array | — | Custom container definitions |

### Memory Core Options

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `dreaming.enabled` | boolean | true | Enable dreaming cycles |
| `dreaming.frequency` | string | cron expr | Dreaming schedule |

## What You Get

### Local (memory-core)
- **QMD search** — fast local vector search over MEMORY.md and workspace files
- **MEMORY.md management** — automatic memory file updates
- **Dreaming** — Light (recent recall), REM (consolidation), Deep (pruning) phases
- **Flush plans** — controlled memory writes

### Cloud (SuperMemory)
- **Cross-session persistence** — memories survive restarts, compaction, model switches
- **Cross-device sync** — same memories on Mac Mini, Mac Studio, mobile
- **Entity context** — user profiles and preferences injected automatically
- **Custom containers** — isolate memories per agent or project

### Composite Benefits
- **Merged search** — queries both backends, deduplicates results by relevance score
- **Dual recall** — local QMD results + cloud SuperMemory context injected together. Writes go to memory-core (local MEMORY.md); SuperMemory captures conversation content automatically via its auto-capture hook.
- **Dreaming** — runs natively through memory-core's consolidation cycle (Light/REM/Deep phases)
- **Single slot** — clean config, no hacks

## Architecture

### Proxy Pattern

The plugin creates proxy `OpenClawPluginApi` objects for each sub-plugin. These proxies intercept:
- `registerMemoryRuntime` — captures the runtime from each backend
- `registerMemoryPromptSection` — captures prompt injection from each
- `registerMemoryFlushPlan` — captures flush plans (memory-core only)

After both sub-plugins register, the composite builds unified versions and registers them on the real API.

### Files

| File | Purpose |
|------|---------|
| `index.ts` | Entry point — loads backends, registers composite |
| `composite-runtime.ts` | Merged memory runtime |
| `composite-prompt.ts` | Merged prompt section |
| `composite-search-manager.ts` | Search merging and deduplication |
| `proxy-api.ts` | Proxy API factory |
| `config.ts` | Config parsing |
| `openclaw.plugin.json` | Plugin manifest |

## Requirements

- OpenClaw >= 2026.1.29
- Node.js 20+
- `openclaw-supermemory` extension (sibling directory)
- SuperMemory API key ([supermemory.com](https://supermemory.com))

## Security Notes

- **No hardcoded tokens or keys** — API keys are read from config or environment variables only
- **Network calls via SuperMemory client** — the plugin instantiates a `SupermemoryClient` for cloud search. This makes HTTPS calls to SuperMemory's API (`api.supermemory.com`) to search and store memories. The client comes from the `openclaw-supermemory` sibling extension. No other network calls are made.
- **Required env var: `SUPERMEMORY_OPENCLAW_API_KEY`** — needed for cloud memory. Get one at [supermemory.com](https://supermemory.com). No other env vars are read.
- **No file system writes** — memory writes are delegated to memory-core's native flush plan
- **No exec/spawn** — no shell commands or child processes
- **Relative sibling imports** — this plugin imports from `../openclaw-supermemory/` because OpenClaw's extension loader requires plugins to be co-located. This is the standard pattern for composite plugins that wrap other extensions

## Troubleshooting

**"both backends failed to load"** — Check that `openclaw-supermemory` exists as a sibling extension and `npm install` was run in both directories.

**"memory-core not available"** — The plugin tries to resolve memory-core from OpenClaw's built-in extensions. Make sure your OpenClaw version is >= 2026.1.29.

**No cloud memories appearing** — Verify `SUPERMEMORY_OPENCLAW_API_KEY` is set in your environment or `.env` file.

**Dreaming not running** — Check that `memoryCore.dreaming.enabled` is true and you have a cron job configured for the dreaming schedule.

## License

MIT
