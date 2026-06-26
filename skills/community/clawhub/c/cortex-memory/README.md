# Cortex Memory - Deployment Guide

Long-term memory system for OpenClaw agents. Automatically recalls relevant past context before each turn and captures new facts after each turn. Provides tools for explicit search, save, forget, and lookup.

## Requirements

- OpenClaw runtime (2026.3.x or later)
- `openclaw-cortex` plugin installed and configured
- Cortex API key

## Installation

### 1. Install the plugin

```bash
openclaw plugin install @ubundi/openclaw-cortex@latest
```

### 2. Configure tools profile

The default `messaging` tools profile excludes memory tools. Set tools to `full`:

```bash
openclaw config set tools.profile full
```

Or selectively allow the cortex tools:

```json
{
  "tools": {
    "alsoAllow": [
      "cortex_search_memory",
      "cortex_save_memory",
      "cortex_forget",
      "cortex_get_memory"
    ]
  }
}
```

### 3. Add API key and plugin config

Edit `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "openclaw-cortex": {
        "enabled": true,
        "config": {
          "apiKey": "your-cortex-api-key"
        }
      }
    }
  }
}
```

Or use an environment variable:

```bash
export CORTEX_API_KEY="your-cortex-api-key"
```

### 4. Install the skill

```bash
mkdir -p ~/.openclaw/skills/cortex-memory
cp skill/SKILL.md ~/.openclaw/skills/cortex-memory/
```

### 5. Restart and verify

```bash
openclaw restart
```

Run an agent turn and check that `<cortex_memories>` tags appear in the agent's context.

## Configuration Options

Add these to the plugin config in `openclaw.json`:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | string | — | Cortex API key (required if no env var) |
| `autoRecall` | boolean | `true` | Auto-inject memories before each turn |
| `autoCapture` | boolean | `true` | Auto-extract facts after each turn |
| `recallTopK` | number | `15` | Max memories to inject per turn |
| `recallTimeoutMs` | number | `3000` | Timeout for recall API calls |
| `toolTimeoutMs` | number | `8000` | Timeout for tool API calls |
| `captureInstructions` | string | — | Custom guidance for auto-capture |
| `captureCategories` | string[] | — | Categories to pay attention to |
| `noveltyThreshold` | number | `0.85` | Similarity threshold for deduplication |
| `auditLog` | boolean | `false` | Enable audit logging by default |

### Example full config

```json
{
  "plugins": {
    "entries": {
      "openclaw-cortex": {
        "enabled": true,
        "config": {
          "apiKey": "your-cortex-api-key",
          "autoRecall": true,
          "autoCapture": true,
          "recallTopK": 15,
          "recallTimeoutMs": 3000,
          "captureInstructions": "Focus on project architecture decisions and team preferences",
          "captureCategories": ["deployment configs", "API contracts", "team conventions"],
          "auditLog": false
        }
      }
    }
  }
}
```

## CLI Commands

The plugin adds CLI commands for managing memory from the terminal:

```bash
openclaw cortex status      # Connection status and session stats
openclaw cortex memories    # List recent memories
openclaw cortex search      # Search memories by query
openclaw cortex config      # Show current plugin configuration
openclaw cortex pair        # Pair with Cortex API (interactive setup)
openclaw cortex info        # Show plugin and API info
openclaw cortex reset       # Reset plugin state
```

When the agent is running in a terminal-capable environment, it should prefer executing these commands for the user and summarizing the output instead of replying with "run this in terminal." The exception is `openclaw cortex reset`, which should only be run after explicit confirmation because it is destructive.

## Agent Commands

These commands are available to the agent during conversation:

- `/checkpoint` — Save session summary before resetting context
- `/sleep` — Mark session as cleanly ended (no recovery warning next time)
- `/audit on|off` — Toggle local audit logging of Cortex API calls

## Testing Checklist

### Auto-recall
- [ ] Start a conversation and verify `<cortex_memories>` tags appear
- [ ] Memories are relevant to conversation topic
- [ ] Confidence scores are included

### Tools
- [ ] `cortex_search_memory` returns results for known topics
- [ ] `cortex_save_memory` accepts and confirms saves
- [ ] `cortex_save_memory` with `checkNovelty: true` skips duplicates
- [ ] `cortex_forget` with `query` finds candidate memories
- [ ] `cortex_forget` with `entity` removes memories
- [ ] `cortex_get_memory` retrieves by node ID

### Auto-capture
- [ ] After a conversation turn, new facts appear in subsequent recalls
- [ ] Volatile state (versions, ports) is stripped from captures

### Commands
- [ ] `/checkpoint` saves session summary
- [ ] `/sleep` clears recovery state
- [ ] `/audit on` enables logging, `/audit off` disables

### CLI
- [ ] `openclaw cortex status` shows connection info
- [ ] `openclaw cortex search "query"` returns results

## Troubleshooting

### No memories recalled
- Check plugin is enabled: `openclaw cortex status`
- Verify API key is valid: `openclaw cortex pair`
- Check `autoRecall` is not set to `false`
- Ensure memories exist: `openclaw cortex search "test"`

### Saves failing
- Check API connectivity: `openclaw cortex status`
- Verify API key permissions
- Check audit log for error details: `/audit on`, then retry

### Stale memories being recalled
- Use `cortex_forget` to remove outdated memories
- Report both memory and live state to the user with timing context

### Plugin not loading
- Verify installation: `openclaw doctor`
- Check for naming issues in config (use `openclaw-cortex` as the plugin key)
- Restart the gateway after installation

## Privacy & Data Handling

**What is captured:**
- Facts, preferences, and decisions stated in conversation
- Conversation transcripts are sent to Cortex API for extraction
- Volatile state (versions, ports, task statuses) is stripped before capture

**What is NOT captured:**
- Raw tool output or debug logs
- File contents (only facts derived from conversation)
- Secrets or credentials (filtered by the capture pipeline)

**User control:**
- Disable auto-capture: Set `autoCapture: false` in config
- Disable auto-recall: Set `autoRecall: false` in config
- Forget specific memories: Use `cortex_forget` tool or `openclaw cortex` CLI
- Audit all data: Enable `/audit on` to log everything sent to Cortex
- All data is scoped per user and per workspace (namespace isolation)

**Data storage:**
- Memories are stored in the Cortex API backend
- Audit logs are stored locally at `<workspace>/.cortex/audit/`
- Session state is stored locally in the OpenClaw data directory

## Support

For issues or questions:
- Work Stream: Skills
- Platform: Kwanda
- Repository: kwanda-skills
