---
name: chatpipe-export
description: >
  Export any AI chat session to Markdown, JSON, or plain text using ChatPipe v1.1.
  Supports 7 input formats including OpenClaw sessions, Hermes agent logs,
  ChatGPT exports, and Chatbox exports. Use when the user asks to export/backup
  their chat history, convert conversations to Obsidian/Notion, or migrate between
  AI platforms. Free skill wraps the open-source ChatPipe engine.
  Triggers: "导出聊天记录", "export chat", "save conversation", "backup my chats",
  "导出到Obsidian", "导出到Notion", "convert to markdown", "chat export".
---

# ChatPipe Export — One-Click AI Chat Export

Export any AI chat session to clean Markdown, JSON, or plain text.
No manual file handling. Just say "export this conversation".

## Supported Formats

### Input (auto-detected)
| Format | Source |
|--------|--------|
| `openclaw-json` | Current / past OpenClaw sessions |
| `hermes-json` | Hermes agent logs |
| `chatgpt-json` | ChatGPT data export ZIP |
| `chatbox-html` | Chatbox exported HTML |
| `chatbox-json` | Chatbox conversations.json |
| `markdown` | Role-labeled .md files |
| `plain-text` | Role-labeled .txt files |

### Output
| Format | Use case |
|--------|----------|
| `markdown` | Obsidian, Notion, GitHub, VS Code |
| `chatgpt-json` | Import into ChatGPT tools, API processing |
| `chatbox-json` | Import back into Chatbox |
| `plain-text` | grep, shell scripts, minimal storage |

## Quick Export

To export the **current session** as Markdown:

```bash
python3 scripts/export_session.py --markdown
```

To export a **past session** by session key:

```bash
python3 scripts/export_session.py agent:main:main --format markdown
```

To export a **Hermes session**:

```bash
python3 scripts/export_session.py agent:hermes:main --format markdown
```

## How It Works

1. Fetch the session transcript via OpenClaw API or file system
2. Pass it through ChatPipe (auto-detects format)
3. Save the output to the workspace

The helper script `scripts/export_session.py` wraps both the data extraction
and ChatPipe conversion into a single command.

## When to Use

| User says | Do this |
|-----------|---------|
| "导出这段聊天" | Export current session as Markdown |
| "保存到Obsidian" | Export to Markdown, tell user where the file is |
| "backup my AI chats" | Export all recent sessions as Markdown batch |
| "convert to JSON" | Export current session as chatgpt-json |
| "导出和Akira的对话" | Find Hermes session, export as Markdown |

## Output Location

Exported files are saved to the workspace root with descriptive names:
`session-{key}-{date}.md`

Never delete or move exported files unless the user explicitly asks.
