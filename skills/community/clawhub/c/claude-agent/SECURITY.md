# Security & Privacy

`claude-agent` is designed for reviewability first. The skill is small, text-only, and its execution paths are limited to:

- `hooks/on_complete.py`
- `hooks/pane_monitor.sh`
- `hooks/start_claude.sh`
- `hooks/stop_claude.sh`

## Runtime boundary

- No bundled third-party npm or pip runtime dependencies are shipped in this repository.
- The Python hook uses only the standard library.
- The shell scripts depend on user-installed `bash`, `tmux`, `openclaw`, and `claude`.
- The skill itself writes only temporary monitor/log files under `/tmp` plus the project changes explicitly made through Claude Code in the chosen working directory.

## Network/data flow

- `claude-agent` does not open arbitrary outbound network connections on its own.
- User-visible notifications are sent through the user's configured OpenClaw message channel.
- OpenClaw wake events are also routed through the user's configured OpenClaw channel.
- As of `2.1.0`, notifications default to `event` mode: they do not include working directory paths or Claude response summaries unless the user opts in.

## Hardening defaults

- Default notification mode is `event`.
- Default wake payload excludes Claude response summaries.
- Approval notifications can be reduced to event-only mode.
- No wildcard filesystem permissions are declared in-project; users should grant only the minimum `Claude Code` tool permissions needed for their workload.

## Recommended operator settings

- Keep `CLAUDE_AGENT_NOTIFY_MODE=event` for private repositories.
- Only enable summary/full notifications in trusted private channels.
- Review `~/.claude/settings.json` and avoid broad `permissions.allow` rules such as unrestricted `Bash(*)`.
- Audit your OpenClaw channel/account configuration before using this skill with production code or secrets.
