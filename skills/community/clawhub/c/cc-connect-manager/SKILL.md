---
name: cc-connect-manager
description: >
  Manage cc-connect projects: add new projects to ~/.cc-connect/config.toml, set up
  multi-agent relay bindings, and restart cc-connect in tmux. Use when the user wants to:
  add a project to cc-connect, configure a new bot/platform binding, remove a project,
  restart cc-connect, set up multiple agents (Claude Code + Codex/Cursor/Gemini) in the
  same chat group with relay/bind. Triggers on: "add project to cc-connect", "connect this
  project to telegram/discord/feishu", "restart cc-connect", "add a new bot", "bind this
  workspace to a platform", "add codex/cursor agent", "set up two agents in the same channel".
---

# cc-connect Manager

Manage cc-connect projects by editing `~/.cc-connect/config.toml` and restarting the service in tmux.

## Config file

Path: `~/.cc-connect/config.toml`

## Add a project

Extract these from the user's request:
- **name**: project name (derive from work_dir basename if not given, e.g. `/path/to/my-app` → `my-app`)
- **work_dir**: absolute path to the project directory
- **platform**: one of `telegram`, `discord`, `feishu`, `dingtalk`, `slack`, `line`, `wecom`, `qq`, `qqbot`
- **token**: the bot token (varies by platform)
- **agent**: default `claudecode`, or `codex`, `cursor`, `gemini`, `qoder`, `opencode`, `iflow`
- **mode**: default `default`. For claudecode: `acceptEdits`/`plan`/`bypassPermissions`. For codex: `suggest`/`auto-edit`/`full-auto`/`yolo`

Run the add script:

```bash
python3 ~/.claude/skills/cc-connect-manager/scripts/add_project.py \
  --name <name> --work-dir <work_dir> --platform <platform> --token <token> \
  [--agent <agent>] [--mode <mode>] [--guild-id <id>]
```

Platform-specific token mapping:
- **telegram**: `--token` = bot token from @BotFather
- **discord**: `--token` = bot token, optionally `--guild-id` for instant slash commands
- **feishu**: `--app-id` + `--app-secret`
- **dingtalk**: `--app-id` + `--app-secret`
- **slack**: `--bot-token` (xoxb-) + `--app-token` (xapp-)

After adding, read back `~/.cc-connect/config.toml` and show the user the new project block for confirmation.

## Multi-agent relay setup (bind)

To put multiple agents (e.g. Claude Code + Codex) in the same chat group:

### Architecture
- Each agent needs its **own bot** (separate token) as a separate `[[projects]]` entry
- All bots join the same group/channel/server
- After startup, use `/bind` in the chat to link them for relay communication

### Step-by-step
1. Add project A (e.g. `claude-backend`, agent=claudecode, platform=discord, token=bot-A-token)
2. Add project B (e.g. `codex-backend`, agent=codex, platform=discord, token=bot-B-token)
3. Both bots must use the **same platform type** and join the **same group/channel**
4. Restart cc-connect
5. Tell the user to send these commands **in the chat group** (not here):
   ```
   @bot-A /bind claude-backend
   @bot-A /bind codex-backend
   ```
   Or for any bot that supports slash commands: `/bind <project-name>`
6. After binding, agents can relay messages to each other. @bot-A sends to Claude Code, @bot-B sends to Codex

### Important notes
- `/bind` is a **runtime chat command**, not a config file setting — it cannot be automated from here
- Binding persists in `~/.cc-connect/relay_bindings.json`
- Each bot in the group needs a unique token (you cannot reuse the same bot for two projects)

## Remove a project

Read `~/.cc-connect/config.toml`, find the `[[projects]]` block with matching name, remove it and all its sub-sections (`[projects.agent]`, `[projects.agent.options]`, `[[projects.platforms]]`, `[projects.platforms.options]`) up to the next `[[projects]]` or global section. Write the file back.

## Restart cc-connect

cc-connect runs in a tmux session named `cc-connect`. To restart:

```bash
# Kill existing cc-connect process in tmux and start fresh
tmux send-keys -t cc-connect C-c && sleep 1 && tmux send-keys -t cc-connect 'cc-connect' Enter
```

If the tmux session doesn't exist yet:

```bash
tmux new-session -d -s cc-connect 'cc-connect'
```

Always restart after adding or removing a project.

## Workflow

1. Parse the user's natural language request to extract project params
2. Run `add_project.py` for each project (or manually edit for removal)
3. Show the user the updated config block
4. Restart cc-connect in tmux
5. Confirm success by checking tmux output: `tmux capture-pane -t cc-connect -p | tail -5`
6. If multi-agent setup, remind the user to run `/bind <project-name>` for each project in the chat group
