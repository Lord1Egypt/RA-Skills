---
name: cli-hub
description: >-
  Unified CLI gateway to search, install, authenticate, and invoke enterprise
  and AI platform tools (WeCom, DingTalk, Lark/Feishu, Dreamina) covering
  91+ operations. Use when the user mentions WeCom, DingTalk, Lark, Feishu,
  Dreamina, or needs to send messages, manage calendars, todos, contacts,
  documents, meetings, generate images/videos, or AI-powered creation.
---

# cli-hub — Unified CLI Gateway

One Skill to search and invoke all enterprise and AI creation tools (WeCom / DingTalk / Lark / Dreamina), covering 91+ tools.

## Installation

**Recommended (from PyPI, package signatures verified):**

```bash
pip install agent-cli-hub     # pip
pipx install agent-cli-hub    # pipx (isolated env)
uv tool install agent-cli-hub # uv
```

> PyPI: https://pypi.org/project/agent-cli-hub/
> Source: https://github.com/agentrix-ai/clihub (MIT License)

**Alternative (convenience script, internally runs pip from PyPI):**

```bash
curl -sSL https://raw.githubusercontent.com/agentrix-ai/clihub/main/install.sh | bash
```

After installation, `cli-hub` is available as a command.

## Mandatory Rules

1. **Never guess commands** — Always `cli-hub search` to find the tool ID first.
2. **Check params before calling** — Always `cli-hub info <id>` to confirm the parameter schema.
3. On error, consult the "Error Handling" table below.

## Standard Workflow

Follow Steps 1 → 2 → 3 → 4 strictly in order.

### Step 1: Check Environment (required on first use)

```bash
cli-hub doctor
```

Based on output:
- `not installed` → install the CLI
- `installed` but not authenticated → run auth
- All OK → skip to Step 2

**Install underlying CLIs:**

```bash
cli-hub install wecom              # WeCom
cli-hub install dingtalk           # DingTalk
cli-hub install lark               # Lark/Feishu
cli-hub install dreamina           # Dreamina AI
cli-hub install --all              # All providers
cli-hub install lark --timeout 300 # Increase timeout for slow networks
```

**Authenticate (interactive, requires browser):**

```bash
cli-hub auth wecom
cli-hub auth dingtalk
cli-hub auth lark
cli-hub auth dreamina              # Dreamina (terminal QR code login)
cli-hub auth --status              # Check all auth status
```

### Step 2: Search Tools

```bash
cli-hub search "send message"
cli-hub search "create todo" --provider lark
cli-hub search "generate video" --provider dreamina
cli-hub search "meeting" --json     # Recommended for agents: JSON with input_schema
```

### Step 3: Check Parameters

```bash
cli-hub info wecom.msg.send_message        # Table format
cli-hub info wecom.msg.send_message --json # Recommended for agents: full JSON Schema
```

Shows: parameter name, type, required (`*`), example, command template.

### Step 4: Invoke Tool

**Method A — JSON arguments (WeCom style):**

```bash
cli-hub run wecom.msg.send_message --args '{"chat_type":1,"chatid":"user1","msgtype":"text","text":{"content":"hello"}}'
```

**Method B — Flag arguments (DingTalk / Lark / Dreamina style):**

```bash
cli-hub run lark.im.messages_send --chat-id oc_xxx --text "Hello"
cli-hub run dingtalk.todo.task_create --title "Write report" --executors userId
cli-hub run dreamina.generate.text2image --prompt "a cat portrait" --ratio 1:1
```

**How to choose?** `cli-hub info <id>` Example field shows the underlying CLI's argument style.

## Utility Commands

| Command | Purpose |
|---------|---------|
| `cli-hub list` | List all providers |
| `cli-hub list lark` | List all Lark tools |
| `cli-hub list dingtalk --category todo` | Filter by category |
| `cli-hub refresh` | Refresh schemas from installed CLIs |
| `cli-hub add <binary> --display "Name"` | Add a new CLI provider |

## Decision Tree

```
User intent
├── Unsure which platform → cli-hub search "<description>"
├── Know platform, not tool → cli-hub list <provider>
├── Found tool ID → cli-hub info <id> → cli-hub run <id> [args]
├── "not installed" → cli-hub install <provider>
├── "not authenticated" → cli-hub auth <provider>
├── "Operation not found" → cli-hub search again
├── "timed out" → cli-hub install <provider> --timeout 300
└── Unsure about env → cli-hub doctor
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `not installed` | CLI not installed | `cli-hub install <provider>` |
| `not authenticated` | Not authenticated | `cli-hub auth <provider>` |
| `Operation not found` | Typo in ID | `cli-hub search` to find correct ID |
| `No adapter registered` | Wrong provider name | `cli-hub list` to see available names |
| `timed out after Ns` | Timeout | Retry with `--timeout 300` |
| `Invalid JSON` | Malformed --args JSON | Check quotes and escaping |
| Underlying CLI error | Wrong params or insufficient permissions | `cli-hub info <id>` to check params |

## Supported Platforms

| Platform | Provider | Tools | Coverage |
|----------|----------|-------|----------|
| WeCom (企业微信) | wecom | 28 | Contacts, Todos, Meetings, Messages, Calendars, Docs, Smart Sheets |
| DingTalk (钉钉) | dingtalk | 23 | Contacts, Groups, Calendar, Todos, Approvals, Attendance, Logs, Smart Sheets |
| Lark/Feishu (飞书) | lark | 28 | Calendar, Messages, Docs, Drive, Bitable, Spreadsheets, Tasks, Wiki, Email, Meetings |
| Dreamina (即梦) | dreamina | 12 | Text-to-Image, Text-to-Video, Image-to-Video, Multimodal Video, Upscale, Seedance 2.0 |

## Notes

- Authentication is interactive; the agent should prompt the user to complete browser authorization
- For Dreamina, use `dreamina login --headless` (terminal QR code); generation consumes credits — warn the user
- Dreamina tasks are async: after submit, use `query_result --submit_id=<id>` to check results
- Search results are ranked by relevance; prefer the highest-scored tool
- Invoke tools one at a time and confirm results before proceeding
