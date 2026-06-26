---
name: claude-quota-checker
description: "Check how much Claude Max / Claude Pro subscription quota you have LEFT — not how much you spent. Most usage tools track API billing or token costs. This one answers the real question: 'Am I about to hit my limit?' Shows remaining % for session and weekly windows, plan type, and exact reset times. Works by automating Claude Code CLI's /usage command via tmux — no API keys, no Admin keys, no reverse engineering. Just your subscription status, instantly. Use whenever someone asks: 'how much Claude do I have left', 'am I rate limited', 'when does my quota reset', 'check my usage', 'claude limits', '还剩多少', '查用量', '还能用吗', 'why is Claude slow'. Also use as a first diagnostic when the user hits rate limits or Claude feels sluggish."
---

# Claude Quota Checker

**How much Claude do you have LEFT?**

Most tools tell you how much you *spent*. This one tells you how much you have *remaining* — the question that actually matters when you're working and worried about hitting limits.

Checks your Claude Max/Pro subscription quota by automating the `/usage` command via tmux. No API keys needed, no Admin keys, no complex setup.

## How It Works

1. Creates a temporary tmux session with a scratch git repo
2. Launches Claude Code CLI
3. Handles the "trust this folder" prompt automatically
4. Sends `/usage` command
5. Captures and parses the output
6. Cleans up tmux session

## Usage

```bash
bash ./scripts/check-usage.sh
```

> **Note**: Run from the skill directory, or use the full path based on where you installed this skill. The script auto-detects its own location.

## Output

- **Plan type**: Pro or Max (e.g., "Opus 4.6 — Claude Max")
- **Session usage**: current session % used
- **Weekly usage**: all models % and Sonnet-only %
- **Reset time**: when the weekly quota resets

## Error Handling

| Problem | Symptom | Fix |
|---------|---------|-----|
| tmux not installed | `command not found: tmux` | `brew install tmux` |
| Claude CLI not in PATH | Session hangs | Install Claude Code CLI, ensure `claude` is in PATH |
| Auth expired | "Please log in" in output | Run `claude` manually and re-authenticate |
| Git not installed | Script fails at `git init` | `brew install git` |

If the script hangs for >15 seconds, it likely means Claude CLI couldn't start. Kill with: `tmux kill-session -t cu-*`

## Requirements

- macOS or Linux
- `tmux` installed
- `claude` CLI in PATH
- Active Claude Code authentication (Pro or Max subscription)
- `git` installed (for scratch repo)

## Performance

~8-10 seconds (bottleneck: Claude Code CLI startup time).

## Limitations

- Only checks **subscription** usage (Pro/Max), not API billing
- Requires a running terminal environment (won't work in sandboxed containers)
- Output parsing depends on Claude Code CLI's `/usage` format — may break if Anthropic changes the output layout
