# dual-memory

A dual-memory plugin for OpenClaw that combines **local memory-core** (with dreaming/consolidation) and **SuperMemory** (cloud persistence) into a single memory slot using a proxy pattern.

## Why

OpenClaw only allows one plugin per `kind: "memory"` slot. This plugin legitimately holds that slot and delegates to both backends:

- **memory-core** → Local vector search (QMD), MEMORY.md management, and native dreaming (Light/REM/Deep phases)
- **SuperMemory** → Cloud-based persistent memory that survives across sessions, devices, and agent instances

Both systems run simultaneously. Searches query both backends and merge results. Writes go to both.

## Install

1. Copy the plugin to your extensions directory:
```bash
cp -r dual-memory ~/.openclaw/extensions/
cd ~/.openclaw/extensions/dual-memory
npm install
```

2. **Important**: The plugin imports `openclaw-supermemory` as a sibling extension. Make sure you also have:
```
~/.openclaw/extensions/openclaw-supermemory/
```
You can install it from: https://clawhub.ai/skills/supermemory

3. Disable the individual plugins (the composite replaces them):
```yaml
# In your openclaw config, disable these:
plugins:
  entries:
    memory-core:
      enabled: false
    openclaw-supermemory:
      enabled: false
```

The composite plugin auto-loads both internally.

## Configuration

```yaml
plugins:
  entries:
    dual-memory:
      enabled: true
      config:
        supermemory:
          apiKey: "${SUPERMEMORY_OPENCLAW_API_KEY}"
          containerTag: "my_agent_name"  # optional, defaults to hostname
          autoRecall: true
          autoCapture: true
          maxRecallResults: 5
          captureMode: "everything"
          debug: false
        memoryCore:
          dreaming:
            enabled: true
            frequency: "30 2 * * *"  # 2:30 AM daily
```

### SuperMemory Config

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `apiKey` | string | `$SUPERMEMORY_OPENCLAW_API_KEY` | SuperMemory API key (supports `${ENV_VAR}` syntax) |
| `containerTag` | string | hostname | Isolates memories per agent/machine |
| `autoRecall` | boolean | true | Auto-inject relevant memories into conversations |
| `autoCapture` | boolean | true | Auto-store important information |
| `maxRecallResults` | number | 5 | Max memories injected per conversation (1-20) |
| `captureMode` | string | "everything" | What to capture: "everything" or "all" |
| `debug` | boolean | false | Verbose logging |

### Memory Core Config

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `dreaming.enabled` | boolean | true | Enable dreaming consolidation |
| `dreaming.frequency` | string | cron expression | When to run dreaming cycles |

## How It Works

### Architecture

```
dual-memory (holds the memory slot)
├── Proxy API → memory-core (local)
│   ├── QMD vector search
│   ├── MEMORY.md management
│   └── Dreaming (Light/REM/Deep)
└── Proxy API → supermemory (cloud)
    ├── Cloud vector search
    ├── Cross-session persistence
    └── Profile/entity context
```

### Proxy Pattern

The plugin creates proxy API objects that intercept `registerMemoryRuntime`, `registerMemoryPromptSection`, and `registerMemoryFlushPlan` calls from each sub-plugin. It captures their registrations, then composes them into a unified runtime that OpenClaw sees as a single memory provider.

### Search Merging

When the agent searches memory, both backends are queried:
- Local QMD results (file-based, fast)
- SuperMemory cloud results (cross-session, persistent)

Results are merged and deduplicated before returning to the agent.

### Write Flow

Memory writes go to both backends:
- memory-core updates local MEMORY.md and QMD index
- SuperMemory stores to the cloud container

## Requirements

- OpenClaw >= 2026.1.29
- `openclaw-supermemory` extension installed as sibling
- SuperMemory API key (get one at https://supermemory.com)
- Node.js 20+

## Files

| File | Purpose |
|------|---------|
| `index.ts` | Plugin entry — loads both backends via proxies, registers composite |
| `composite-runtime.ts` | Merged memory runtime (search, store, recall) |
| `composite-prompt.ts` | Merged prompt section injection |
| `composite-search-manager.ts` | Search result merging and deduplication |
| `proxy-api.ts` | Proxy API factory that captures sub-plugin registrations |
| `config.ts` | Config parsing and validation |
| `openclaw.plugin.json` | Plugin manifest |

## License

MIT
