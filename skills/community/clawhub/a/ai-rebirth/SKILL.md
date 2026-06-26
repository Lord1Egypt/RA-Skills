---
name: ai-rebirth
description: "AI Rebirth - Load conversation history from a previous CodeBuddy session into the current session. Use when the user wants to resume, reference, or continue a previous session's work. Supports session ID lookup, project-based listing, summary and full output modes."
description_zh: "AI 重生 - 加载历史 Session 对话，延续前世记忆"
description_en: "AI Rebirth - Load previous session history into current session"
version: 1.0.0
allowed-tools: Read,Bash,Grep
---

# AI Rebirth

AI 重生 - 让新的 session 继承前世的记忆。加载并展示之前 CodeBuddy session 的对话历史，用于恢复中断的工作或导入其他 session 的上下文。

## Core Script

`scripts/load_session.py`

After installing, copy `scripts/load_session.py` to `~/.codebuddy/bin/load_session.py` for easy access.

## Usage

### List sessions for current project

```bash
python3 scripts/load_session.py --project /path/to/project
```

### Load a specific session (summary mode, default)

```bash
python3 scripts/load_session.py --id <SESSION_UUID>
```

### Load full message chain

```bash
python3 scripts/load_session.py --id <SESSION_UUID> --mode full
```

### Load last N turns

```bash
python3 scripts/load_session.py --id <SESSION_UUID> --mode "tail 5"
```

## Output Modes

| Mode | Description |
|------|-------------|
| `summary` | Structured summary: stats, topics, user requests, last 3 turns (default) |
| `full` | Complete message chain in Markdown |
| `tail N` | Last N conversation turns (user+assistant pairs) |

## Workflow

1. User asks to load/resume/reference a previous session
2. If no session ID given, list available sessions for the current project
3. User selects or provides a session ID (can paste partial conversation to help identify)
4. Run the script with chosen mode
5. Present the output to the user as context for continuing work

## How It Works

- Reads session JSONL files from `~/.codebuddy/projects/<project-name>/`
- Extracts `type=message` records (user and assistant messages)
- Extracts `type=topic` records for conversation topic tracking
- Generates structured Markdown output

## Notes

- Read-only: never modifies source session data
- No external dependencies, pure Python 3 standard library
- Handles large JSONL files (4MB+) via line-by-line streaming
- Project directory name is derived from the working directory path (slashes replaced with dashes)
