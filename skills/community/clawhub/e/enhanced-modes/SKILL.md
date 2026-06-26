# Enhanced Agent Modes 🦞

Three working modes: Explore (read-only), Plan (think before act), Verify (check results). Plus feature flags for toggling capabilities.

> Inspired by Claude Code source leak analysis (v2.1.88)

## Installation

```bash
npx clawhub install enhanced-modes
# or
npx clawhub install <this-skill-repo>
```

## Quick Reference

| Command | Function |
|---------|----------|
| `/mode explore` | Switch to read-only exploration mode |
| `/mode plan` | Switch to planning mode (think before acting) |
| `/mode verify` | Switch to verification mode (check after doing) |
| `/mode normal` | Return to normal mode |
| `/features` | Show available feature flags |
| `/features enable <name>` | Enable a feature |
| `/features disable <name>` | Disable a feature |

## Explore Mode

When user types `/mode explore` or asks to "search only":

1. **System prompt**: "You are in EXPLORE MODE - READ ONLY. Do NOT modify any files. Do NOT execute commands that change state."
2. **Tool restrictions**:
   - ✅ READ: FileRead, Glob, Grep, WebFetch
   - ❌ DENY: FileWrite, FileEdit, Bash, exec
3. **Response format**: Provide findings as analysis, not actions
4. **Exit**: User says "exit explore" or `/mode normal`

## Plan Mode

When user types `/mode plan` or asks to "plan first":

1. **System prompt**: "You are in PLAN MODE - Think before acting. Analyze the request, consider approaches, then present a plan before executing."
2. **Behavior**:
   - Analyze request thoroughly
   - Consider 2-3 alternative approaches
   - Present pros/cons of each
   - Wait for user approval before executing
3. **Exit**: User approves plan or says "exit plan" or `/mode normal`

## Verify Mode

When user types `/mode verify` or asks to "verify results":

1. **System prompt**: "You are in VERIFY MODE - Check results after actions. Do not assume success. Verify each step."
2. **Behavior**:
   - After any action, verify the outcome
   - Check file contents, command output, API responses
   - Report actual vs expected results
   - Flag any discrepancies
3. **Exit**: User says "exit verify" or `/mode normal`

## Feature Flags

Features can be enabled/disabled dynamically:

| Feature | Default | Description |
|---------|---------|-------------|
| `deep_thinking` | true | Enable extended reasoning for complex problems |
| `auto_memory` | false | Automatically consolidate memories periodically |
| `coordinator_mode` | false | Enable multi-worker coordination |
| `wal_protocol` | true | Write corrections/decisions before responding |
| `working_buffer` | true | Log exchanges in danger zone (>60% context) |
| `explore_agent` | true | Enable built-in Explore Agent |
| `plan_agent` | true | Enable built-in Plan Agent |
| `verify_agent` | false | Enable built-in Verification Agent |
| `proactive_checkins` | false | Periodic proactive suggestions |
| `autonomous_crons` | false | Background autonomous tasks |

### Using Features

```
/features           # Show all features
/features enable auto_memory
/features disable verify_agent
```

## Auto-Memory Consolidation

When `auto_memory` feature is enabled:

### Trigger Conditions
- Context > 60% (danger zone entered)
- Session ends
- User requests consolidation

### Process
1. Scan daily memory files for important content
2. Extract decisions, preferences, context
3. Update long-term memory
4. Archive raw notes

## Background Tasks

When `autonomous_crons` feature is enabled:

### Task Types
| Type | Trigger | Execution |
|------|---------|-----------|
| `systemEvent` | Timer fires | Prompt to main session |
| `isolated agentTurn` | Timer fires | Spawn sub-agent |

### When to Use Each
- **systemEvent**: Interactive tasks needing user attention
- **isolated agentTurn**: Background maintenance, checks, updates

## Architecture

```
skills/enhanced-modes/
├── SKILL.md              # This file
└── assets/
    └── SESSION-STATE.md  # Mode and feature state
```

## Credits

- Inspired by Claude Code source leak (v2.1.88)
- Patterns adapted from Proactive Agent skill
- Feature flag system inspired by GrowthBook

## License

MIT - Free to use, modify, distribute
