---
name: agent-config-manager
description: Manage OpenClaw agent configurations, update models, modify bindings, and test configuration changes. Use when: (1) Updating agent model assignments, (2) Modifying channel bindings, (3) Adding/removing agents, (4) Testing config changes before apply, (5) Backing up/restoring agent configs, (6) Validating configuration syntax. Safe editing with validation and rollback support.
---

# Agent Config Manager

Safe management of OpenClaw agent configurations with validation and rollback.

## Quick Start

### List all agents
```bash
scripts/list_agents.sh
```

### Update agent model
```bash
scripts/set_agent_model.sh cybercodeur openrouter/google/gemini-2.5-flash
```

### Test configuration (dry-run)
```bash
scripts/test_config.sh --dry-run
```

### Backup & restore
```bash
scripts/backup_config.sh
scripts/restore_config.sh <backup_date>
```

## Core Operations

### Change Agent Model
```bash
scripts/set_agent_model.sh <agent_id> <new_model>
# Examples:
scripts/set_agent_model.sh snake google/gemini-2.5-flash
scripts/set_agent_model.sh all moonshotai/kimi-k2.5  # Set all to same model
```

**Validation**: 
- Model exists in configured list? ✓
- Model format correct (provider/model)? ✓
- Config syntax valid (jq)? ✓

### Add Fallback Chain
```bash
scripts/add_fallback.sh cybercodeur \
  --primary google/gemini-2.5-flash \
  --fallback1 deepseek/deepseek-v3.2 \
  --fallback2 moonshotai/kimi-k2.5
```

### Update Multiple Agents
```bash
scripts/bulk_update.sh \
  --agents cybercodeur snake picsou \
  --model qwen/qwen3-coder-plus
```

## Workflow: Solution 2 (Fallbacks)

To implement Solution 2 (automatic fallback on rate limit):

```bash
scripts/add_fallback.sh cybercodeur \
  --primary qwen/qwen3-coder-plus \
  --fallback1 deepseek/deepseek-v3.2 \
  --fallback2 google/gemini-2.5-flash

scripts/test_config.sh --validate
openclaw gateway restart
```

## Safety Features

- **Dry-run mode**: Test changes without applying
- **Automatic backup**: Every change backs up to `/tmp/openclaw-config.bak`
- **Validation**: Syntax & model existence checks
- **Rollback**: Restore previous config in seconds

## Files

- **scripts/list_agents.sh** - List agent configs
- **scripts/set_agent_model.sh** - Update single agent model
- **scripts/add_fallback.sh** - Configure fallback chains
- **scripts/bulk_update.sh** - Update multiple agents
- **scripts/test_config.sh** - Validate config
- **scripts/backup_config.sh** - Manual backup
- **scripts/restore_config.sh** - Restore from backup
