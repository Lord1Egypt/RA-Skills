---
name: browser-recover
description: Recover the local Chromium/Chrome environment when browser tool calls fail. Use when encountering (1) Browser startup failures, (2) CDP connection errors (Target closed, ECONNREFUSED, timeout), (3) Stale browser processes blocking new instances, (4) Port conflicts on 9222/18800, (5) Browser page freezes causing subsequent tool calls to fail. Automatically kills stale processes, clears lock files, releases ports, and retries the original browser task once.
---

# Browser Recover

Automated recovery for OpenClaw browser environment failures.

## Quick Start

When a browser tool call fails, follow this workflow:

1. **Detect**: Check if error matches browser environment issues
2. **Diagnose**: Run `scripts/check_state.sh` to inspect current state
3. **Recover**: Run `scripts/recover.sh` to clean up
4. **Retry**: Execute the original browser operation ONCE
5. **Report**: If still fails, output error summary and STOP

## Error Pattern Matching

| Error Pattern | Likely Cause | Recovery Action |
|---------------|--------------|-----------------|
| `Target closed` | Stale CDP connection | `recover.sh --kill-processes` |
| `ECONNREFUSED` on port 9222/18800 | Port conflict | `recover.sh --clear-ports` |
| `timeout` during browser.start | Lock file conflict | `recover.sh --clear-locks` |
| Multiple chromium processes | Zombie processes | `recover.sh --full` |
| `Profile in use` | Stale lock files | `recover.sh --clear-locks` |

## Recovery Scripts

### check_state.sh
Diagnose browser environment without making changes.

**Usage:**
```bash
bash scripts/check_state.sh
```

**Output:**
- Browser process count and PIDs
- Port usage status (9222, 18800, custom ports)
- Lock file locations
- Recommendation (clean or no action needed)

### recover.sh
Clean up stale browser resources.

**Usage:**
```bash
# Full recovery (default)
bash scripts/recover.sh

# Specific actions
bash scripts/recover.sh --kill-processes
bash scripts/recover.sh --clear-ports
bash scripts/recover.sh --clear-locks

# Explicit full recovery
bash scripts/recover.sh --full
```

**Actions:**
1. Kills stale browser processes (chromium, chrome variants)
2. Clears port conflicts (9222, 18800, configured ports)
3. Removes lock files (SingletonLock, SingletonSocket, SingletonCookie)
4. Clears cache directories (Cache, Code Cache, GPUCache)
5. Waits 2 seconds for resources to release

**Configuration:**
- Reads `~/.openclaw/config/openclaw.json` for browser settings
- Falls back to defaults if config not found
- See [references/configuration.md](references/configuration.md) for details

## Retry Policy

**Session-level tracking:**
- Maximum 2 recovery attempts per session
- Track failures to prevent infinite loops
- Stop after 2nd failure and escalate to human

**Implementation:**
```
Attempt 1: browser fails → diagnose → recover → retry → success ✓
Attempt 2: browser fails → diagnose → recover → retry → fails → STOP
```

**When to stop:**
- 2nd recovery in same session fails
- Error is not browser-environment related
- System-level issues detected (permissions, resources)
- User explicitly requests manual intervention

## Safety Constraints

**DO:**
- Only clean OpenClaw-managed browser instances
- Verify process ownership before killing
- Check profile path matches `~/.openclaw/browser`
- Log all actions to stderr for OpenClaw to capture

**DON'T:**
- Kill user's personal browser processes
- Delete user profile directories (`~/.config/chrome`, etc.)
- Use `kill -9` without verification
- Restart entire system
- Clean up other agents' browser instances without isolation

See [references/safety.md](references/safety.md) for detailed guidelines.

## Troubleshooting

If recovery fails or behaves unexpectedly:

1. Run `check_state.sh` to diagnose
2. Check OpenClaw logs: `~/.openclaw/logs/`
3. Verify configuration: `~/.openclaw/config/openclaw.json`
4. Review [references/troubleshooting.md](references/troubleshooting.md)
5. If unsure, escalate to human operator

## Configuration

Scripts automatically read OpenClaw config for:
- Browser debug port (`browser.debugPort`)
- Profile directory (`browser.userDataDir`)

See [references/configuration.md](references/configuration.md) for:
- Custom port configuration
- Multiple instance setup
- Platform-specific notes
- Environment variables

## Example Workflow

```markdown
User: "Open https://example.com"
Assistant: [calls browser tool]
Error: "ECONNREFUSED on port 9222"

Assistant: Detected port conflict. Running recovery...
[runs check_state.sh]
[runs recover.sh --clear-ports]
[waits 2 seconds]
[retries browser tool]
Success: Browser opened https://example.com
```

## Notes

- All scripts log to stderr for OpenClaw to capture automatically
- No separate log files are created
- Scripts read OpenClaw config for browser settings
- Recovery is idempotent (safe to run multiple times)
- Maximum 2 recovery attempts per session to prevent loops
