# ClawTK Troubleshooting

## Setup Issues

### "jq is required but not installed"

Install jq:
- macOS: `brew install jq`
- Ubuntu/Debian: `sudo apt install jq`
- Other Linux: check your package manager or download from https://jqlang.github.io/jq/

### "OpenClaw config not found"

Make sure OpenClaw is installed and has been run at least once. The config file should be at `~/.openclaw/openclaw.json`. Run `openclaw doctor` to check your installation.

### Setup completed but changes don't seem active

Restart your OpenClaw gateway after setup:
```
openclaw gateway restart
```

## Spend Guard Issues

### "Daily spend cap reached" blocking my work

Two options:
1. **Temporary bypass**: Say `/clawtk override` for a 1-hour override
2. **Permanent change** (Pro only): Edit `~/.openclaw/clawtk-state.json` and change `spendCaps.daily` to a higher value

### "Retry loop detected" but I'm not in a loop

The retry loop detector triggers when the same tool call runs 3+ times in 60 seconds. If you're intentionally running the same command repeatedly, use `/clawtk override` for a temporary bypass.

### Spend tracking seems inaccurate

ClawTK estimates costs based on average token consumption (~2000 tokens per tool call at ~$0.003/1K tokens). Actual costs vary by model and prompt size. For precise tracking, check your API provider's usage dashboard.

## ClawTK Engine Issues (Pro)

### Engine not found after setup

Check if ClawTK Engine is in your PATH:
```
which rtk
rtk --version
```

If not found:
- Homebrew users: `brew install rtk`
- Others: `curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh`

Then add `~/.local/bin` to your PATH if needed.

### Engine hook not activating

Run `rtk init -g --auto-patch` to reinstall the hook. If using sandbox mode, ensure ClawTK Engine binary is in the sandbox's PATH.

### Engine compressing output I need to see in full

ClawTK Engine compresses output before the LLM sees it, but the full output is still available in your terminal. If you need the LLM to see full output for a specific command, prefix it with `command` to bypass the Engine:
```
command git log --oneline -20
```

## Uninstall

To completely remove ClawTK and restore your original config:
```
/clawtk uninstall
```

This will:
1. Restore your original OpenClaw config from backup
2. Unregister all hooks
3. Remove all ClawTK files (state, spend log, cache)
4. Remove the skill directory

Restart your gateway afterward: `openclaw gateway restart`
