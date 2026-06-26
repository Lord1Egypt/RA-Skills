# Supported AI Engines

## Engine Configuration Table

| Engine ID    | Binary    | Auto-Mode Command                                | Notes                          |
|-------------|-----------|--------------------------------------------------|--------------------------------|
| claude      | claude    | claude --dangerously-skip-permissions            | Richest feature set, agent teams |
| codex       | codex     | codex --full-auto                                | Rust-based, low latency. Needs git repo |
| gemini      | gemini    | gemini                                           | 1M context, Google OAuth login (run `gemini` once to auth) |
| opencode    | opencode  | opencode                                         | 75+ model providers, open-source |
| kimi        | kimi      | kimi                                             | Moonshot AI, ACP compatible    |
| trae        | trae-agent| trae-agent                                       | ByteDance, multi-LLM support   |
| aider       | aider     | aider --yes                                      | Git-first, multi-file coordination |
| goose       | goose     | goose                                            | Block's open-source agent      |

## Adding Custom Engines

Users can add engines by editing `squad.json` in the squad directory. Set:

```json
{
  "engine": "custom",
  "engine_command": "my-agent --auto-mode"
}
```

The watchdog and start scripts will use `engine_command` if present, falling back to the table above for known engine IDs.

## Engine Requirements

- **All engines**: Must support unattended operation (no interactive permission prompts)
- **codex**: Requires a git repository in the working directory. The start script will warn if the target is not a git repo.
- **claude**: `--dangerously-skip-permissions` bypasses all safety prompts. Ensure the working directory contains no sensitive files.
- **gemini**: Uses Google OAuth login (same as Claude Code / Codex). Run `gemini` once in a terminal to complete the browser login flow before starting a squad. No API key needed.
- **opencode**: Configuration via `~/.opencode/config.json`.

## Security Note

All engines run in full-auto mode because the coordinator operates unattended in a tmux session. There is no one to approve permission prompts. Users should:

1. Only point squads at project directories they trust
2. Not store secrets (API keys, credentials) in the coordination directory
3. Use git branches or worktrees for isolation
4. Review the coordinator's commits before merging to main
