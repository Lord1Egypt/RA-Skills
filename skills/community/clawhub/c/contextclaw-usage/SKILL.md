# ContextClaw Plugin Usage

## When to Use

Use this skill when the user asks about:
- Session management or cleanup
- Context usage or token consumption
- Storage space used by sessions
- Pruning old sessions
- Cleaning up orphaned session files
- Session analysis or statistics
- Which sessions are taking up space
- How many messages/tokens in sessions

## Prerequisites

The ContextClaw plugin must be installed:
```bash
npm install -g @rmruss2022/contextclaw
openclaw plugins install @rmruss2022/contextclaw
```

## Quick Start

Check if ContextClaw is installed and running:
```bash
openclaw contextclaw status
```

## Commands

### Analyze Sessions
Get comprehensive analysis of all sessions:
```bash
openclaw contextclaw analyze
```

This shows:
- Total sessions, messages, tokens, storage size
- Largest sessions (top 10)
- Oldest sessions (top 10)
- Orphaned sessions

### Prune Old Sessions
Clean up sessions older than N days (default: 30):
```bash
# Dry run (preview only, safe)
openclaw contextclaw prune --days 30

# Live run (actually deletes)
openclaw contextclaw prune --days 30 --dryRun false
```

**Safety features:**
- Dry run by default (previews before deleting)
- Always keeps main agent sessions
- Always keeps cron sessions
- Shows confirmation before deleting

### Clean Orphaned Sessions
Remove session files not referenced in sessions.json:
```bash
# Dry run
openclaw contextclaw clean-orphaned

# Live run
openclaw contextclaw clean-orphaned --dryRun false
```

### Dashboard
Open the visual session management dashboard:
```bash
openclaw contextclaw dashboard
```
This opens http://localhost:18797

### Quick Stats
Show brief status and statistics:
```bash
openclaw contextclaw status
```

### Configuration
Reconfigure port or OpenClaw home:
```bash
openclaw contextclaw setup
```

## Dashboard Features

The dashboard at http://localhost:18797 provides:
- **Session statistics** - Total sessions, messages, tokens, storage
- **Multiple views** - All, Largest, Oldest, Orphaned, Charts
- **Bar charts** - Visual size distribution
- **Type breakdown** - Sessions by agent type (main, cron, sub-agent)
- **Quick actions** - Prune and clean from UI (preview only)

## Example Usage

**User asks:** "How much storage are my sessions using?"

**Response:**
```bash
openclaw contextclaw analyze
```
Look at the "Total Size" metric in the summary table.

**User asks:** "Clean up old sessions"

**Response:**
```bash
# First preview what would be deleted
openclaw contextclaw prune --days 30

# If approved, run live:
openclaw contextclaw prune --days 30 --dryRun false
```

**User asks:** "Which sessions are taking up the most space?"

**Response:**
```bash
openclaw contextclaw analyze
```
Check the "Largest Sessions" table, or open the dashboard:
```bash
openclaw contextclaw dashboard
```

**User asks:** "Remove orphaned session files"

**Response:**
```bash
# Preview first
openclaw contextclaw clean-orphaned

# If user approves, run live:
openclaw contextclaw clean-orphaned --dryRun false
```

## Session Types

ContextClaw categorizes sessions as:
- **main** - Main agent session (protected from pruning)
- **cron** - Cron job sessions (protected from pruning)
- **subagent** - Spawned sub-agent sessions (can be pruned)
- **unknown** - Unrecognized session types

## Orphaned Sessions

A session is orphaned if:
- `.jsonl` file exists in sessions directory
- Session ID is NOT in `sessions.json`

Common causes:
- Completed sub-agent removed from index
- Manual file operations
- Crashed sessions
- Development/testing

Orphaned sessions are safe to delete.

## Best Practices

1. **Analyze regularly** - Weekly or monthly: `openclaw contextclaw analyze`
2. **Always dry-run first** - Preview before deleting
3. **Adjust age threshold** - 30 days is default, adjust as needed
4. **Review orphaned** - Check before cleaning
5. **Backup if worried** - Though main/cron are protected

## Troubleshooting

If dashboard won't load:
```bash
openclaw contextclaw status  # Check if running
openclaw contextclaw start   # Start if stopped
```

If port is in use:
```bash
openclaw contextclaw setup
# Choose a different port
```

## Technical Details

- **Port:** 18797 (default, configurable)
- **Analysis:** Parses all `.jsonl` files in `~/.openclaw/agents/main/sessions/`
- **Token estimation:** 1 token ≈ 4 characters (approximate)
- **Storage:** Read-only, no database

## Example Output

### Analyze Command
```
📊 Session Analysis

┌──────────────────┬────────┐
│ Metric           │ Value  │
├──────────────────┼────────┤
│ Total Sessions   │ 45     │
│ Total Messages   │ 3,842  │
│ Total Tokens     │ 156,234│
│ Total Size       │ 12.4 MB│
│ Orphaned         │ 8      │
└──────────────────┴────────┘
```

### Prune Command
```
🧹 Session Pruning

⚠️  DRY RUN MODE - No files will be deleted

Sessions older than 30 days:
  ✓ Would delete: 12
  - Would keep: 33
  - Space freed: 4.2 MB

? Run prune in LIVE mode (actually delete files)? (y/N)
```

## Repository

GitHub: https://github.com/rmruss2022/ContextClaw
npm: @rmruss2022/contextclaw
