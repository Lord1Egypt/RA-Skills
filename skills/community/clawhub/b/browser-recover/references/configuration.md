# Browser Recovery Configuration

## OpenClaw Configuration Integration

The recovery scripts automatically read configuration from OpenClaw's config file:

**Config file location**: `~/.openclaw/config/openclaw.json`

### Relevant Browser Configuration

```json
{
  "browser": {
    "debugPort": 9222,
    "userDataDir": "~/.openclaw/browser",
    "executablePath": "/usr/bin/chromium-browser",
    "headless": true
  }
}
```

### Configuration Fields Used by Recovery Scripts

| Field | Purpose | Default |
|-------|---------|---------|
| `browser.debugPort` | CDP debug port to clear | 9222 |
| `browser.userDataDir` | Profile directory to clean | `~/.openclaw/browser` |

## Default Values

If OpenClaw config is not found or doesn't contain browser settings, the scripts use these defaults:

```bash
DEFAULT_PORTS=(9222 18800)
DEFAULT_PROFILE_PATH="$HOME/.openclaw/browser"
```

## Custom Configuration

### Adding Custom Ports

If your environment uses additional debug ports, add them to the OpenClaw config:

```json
{
  "browser": {
    "debugPort": 9222,
    "additionalPorts": [18800, 19222]
  }
}
```

Or modify the recovery script directly:

```bash
# In scripts/recover.sh
DEFAULT_PORTS=(9222 18800 19222)
```

### Custom Profile Paths

If using a non-standard profile location:

```json
{
  "browser": {
    "userDataDir": "/custom/path/to/profiles"
  }
}
```

### Multiple Browser Instances

For environments running multiple OpenClaw instances:

1. **Use unique ports per instance**:
```json
// Instance 1
{"browser": {"debugPort": 9222}}

// Instance 2
{"browser": {"debugPort": 9223}}
```

2. **Use separate profile directories**:
```json
// Instance 1
{"browser": {"userDataDir": "~/.openclaw/browser-1"}}

// Instance 2
{"browser": {"userDataDir": "~/.openclaw/browser-2"}}
```

## Environment Variables

The scripts also respect these environment variables (if set):

```bash
export OPENCLAW_BROWSER_PORT=9222
export OPENCLAW_BROWSER_PROFILE="$HOME/.openclaw/browser"
```

## Platform-Specific Notes

### Linux
- Uses `fuser` or `lsof` for port management
- Requires `pkill` for process cleanup
- Lock files: `SingletonLock`, `SingletonSocket`, `SingletonCookie`

### macOS
- Uses `lsof` for port management (fuser not available)
- Process names may differ: `Google Chrome` vs `chromium`
- Lock files in `~/Library/Application Support/...`

### Docker/Container Environments
- May need `--privileged` flag for process management
- Shared PID namespace considerations
- Volume mounts for profile directories

## Troubleshooting Configuration Issues

### Config File Not Found
```bash
# Check if config exists
ls -la ~/.openclaw/config/openclaw.json

# If missing, scripts will use defaults
```

### Invalid JSON
```bash
# Validate config syntax
jq . ~/.openclaw/config/openclaw.json

# If invalid, scripts will use defaults and log warning
```

### Permission Issues
```bash
# Ensure config is readable
chmod 644 ~/.openclaw/config/openclaw.json

# Ensure profile directory is writable
chmod 755 ~/.openclaw/browser
```
