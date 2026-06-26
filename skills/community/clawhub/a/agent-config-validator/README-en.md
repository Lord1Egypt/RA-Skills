# Agent Config Validator

OpenClaw Agent Configuration Validator - Automated configuration validation tool with security mechanisms

## Overview

Automatically validates the configuration integrity of OpenClaw multi-agent systems, detects outdated references, and supports safe auto-repair.

**Core Security Features:**
- ✅ Read-only mode by default, never modifies anything
- ✅ Safe repair whitelist mechanism
- ✅ Sensitive changes require interactive confirmation
- ✅ Core documents are never auto-modified
- ✅ Automatic backup before any modifications

## Installation

```bash
# Global installation (recommended)
cd agent-config-validator
npm link

# Or use locally
node src/validator.js [options]
```

## Quick Start

### 1. Check Mode (Default, Safe)

```bash
# Check only, no fixes (recommended for first use)
agent-config-validator

# Verbose output
agent-config-validator --verbose
```

### 2. Safe Repair Mode

```bash
# Only repair whitelisted safe items
agent-config-validator --fix --safe-mode
```

### 3. Full Repair Mode (Requires Confirmation)

```bash
# Repair all fixable items (will ask about sensitive changes)
agent-config-validator --fix --confirm-sensitive
```

### 4. Dry Run Mode

```bash
# Shows what will be done, but doesn't execute
agent-config-validator --fix --dry-run
```

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--fix` | `-f` | Enable auto-repair |
| `--safe-mode` | | Only repair whitelist items (enabled by default) |
| `--safe-mode=false` | | Allow repairing non-whitelist items |
| `--confirm-sensitive` | `-c` | Sensitive changes require confirmation |
| `--dry-run` | `-d` | Dry run mode |
| `--verbose` | `-v` | Verbose output |
| `--output <path>` | `-o` | Save report to file |

## Security Design

### Safe Repair Whitelist

The following configuration items can be **safely auto-repaired**:

- `subagents.allowAgents` - Clean up invalid agent references
- `agentToAgent.allow` - Clean up invalid communication permissions
- `bindings` - Clean up invalid bindings

### Configuration Requiring Manual Confirmation

The following configuration changes **require confirmation**:

- `agents.list` - Add/remove agents
- `models.primary` - Primary model change
- `models.fallbacks` - Fallback model changes
- `channels` - Channel configuration
- `auth` - Authentication configuration

### Never Auto-Modified Content

The following core data is **never auto-modified**:

| Type | File | Reason |
|------|------|--------|
| Agent Role Definition | `agents/{agent}/agent/{agent}.md` | Contains role personality |
| Identity Document | `agents/main/agent/IDENTITY.md` | Defines assistant identity |
| Soul/Values | `agents/main/agent/SOUL.md` | Core values |
| Memory Document | `agents/main/agent/MEMORY.md` | User preferences |
| User Preferences | `agents/main/agent/USER.md` | Personalized settings |

## Use Cases

### Scenario 1: After Adding New Agent

```bash
# 1. Manually create agent directory and core documents
# 2. Manually update openclaw.json
# 3. Run validation check
agent-config-validator --verbose

# 4. Safe repair configuration references
agent-config-validator --fix --safe-mode

# 5. Manually update references in other documents
```

### Scenario 2: After Deleting/Merging Agent

```bash
# 1. Remove configuration from openclaw.json
# 2. Run safe repair to clean up references
agent-config-validator --fix --safe-mode

# 3. Manually update documents based on report
```

### Scenario 3: Regular Maintenance

```bash
# Recommended: Run weekly
agent-config-validator --verbose --output report.md
```

## Programming API

```javascript
const AgentConfigValidator = require('agent-config-validator');

const validator = new AgentConfigValidator();

// Basic validation (read-only)
await validator.validate({
    fix: false,
    verbose: true
});

// Safe repair
await validator.validate({
    fix: true,
    safeMode: true
});

// Full repair (with confirmation)
await validator.validate({
    fix: true,
    safeMode: false,
    confirmSensitive: true
});

// Generate report
const report = validator.generateReport('report.md');

// View issues
console.log(validator.issues);

// View fix records
console.log(validator.fixes);
```

## Diagnostic Report

A detailed report is generated after validation:

```markdown
# Agent Config Validation Report
Generated: 2026/3/19 12:00:00

## Summary
- Total Agents: 3
- Errors: 0
- Warnings: 3
- Safe Fixable: 2
- Manual Action Required: 1

## Security Status
✅ Whitelist Repair: Enabled
⚠️ Sensitive Change Confirmation: Required
❌ Document Auto-Repair: Disabled

## Details
### 1. openclaw.json Config Check
⚠️ agentToAgent.allow contains invalid agent [✅ Safe Auto-Repair]

### 2. Document Outdated Check
⚠️ AGENTS.md line 42: References deleted agent [🔒 Protected Document]

## Fix Suggestions
### Safe Auto-Repair
1. Remove invalid agent from agentToAgent.allow
   Command: agent-config-validator --fix --safe-mode

### Manual Action Required
2. Update AGENTS.md line 42
```

## Backup Mechanism

A backup is created before each auto-repair:

```
openclaw.json.backup.1710835200000
```

To restore:

```bash
cp openclaw.json.backup.1710835200000 openclaw.json
```

## Best Practices

1. **Check Before Repair**
   ```bash
   agent-config-validator          # View issues first
   agent-config-validator --fix    # Then execute repair
   ```

2. **Use Dry Run Mode**
   ```bash
   agent-config-validator --fix --dry-run
   ```

3. **Regular Maintenance**
   ```bash
   # Add to scheduled tasks
   0 9 * * 1 agent-config-validator --output weekly-report.md
   ```

4. **Version Control**
   ```bash
   # Commit current config before repair
   git add .openclaw/openclaw.json
   git commit -m "Backup config"
   
   # Run repair
   agent-config-validator --fix
   ```

## Troubleshooting

### Config File Not Found
```
❌ Error: Config file not found
Solution: Run from OpenClaw root, or set OPENCLAW_ROOT environment variable
```

### JSON Syntax Error
```
❌ Error: Cannot load openclaw.json: Unexpected token...
Solution: Manually fix JSON syntax errors
```

### Permission Denied
```
❌ Error: Failed to save config: EACCES
Solution: Ensure write permissions
```

## License

MIT
