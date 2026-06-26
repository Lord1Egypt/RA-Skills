# activity_logger

A minimal OpenClaw skill for logging conversation messages to daily Markdown files.

## Overview

activity_logger automatically saves every conversation (user message + assistant reply) to a daily Markdown file. It creates one file per day in the format `YYYY-MM-DD.md`.

## Features

- 📝 **Daily Log Files** - One Markdown file per day
- ⏰ **Timestamps** - Each entry includes time of conversation
- 🔒 **Append Only** - Never overwrites existing data
- 📁 **Auto-Create** - Creates directories and files automatically
- 📖 **Markdown Format** - Human-readable log format

## Log Format

```markdown
[HH:MM:SS]
User: <message>
Assistant: <reply>
```

## Example

```markdown
[14:30:00]
User: Hello, how are you?
Assistant: I'm doing well, thank you for asking!

[14:32:15]
User: What's the weather like today?
Assistant: Let me check the weather for you.
```

## Installation

```bash
# Clone or download this skill to your OpenClaw skills folder
cp -r activity_logger ~/OpenClawWorkspace/skills/

# Restart OpenClaw gateway
openclaw gateway restart
```

## Log Location

```
workspace/chat/YYYY-MM-DD.md
```

Example path:
```
C:\Users\user\OpenClawWorkspace\chat\2026-03-07.md
```

## How It Works

This skill provides the logic and format for manual logging. The agent appends each conversation turn to the daily log file after responding.

### Core Logic

1. Get current date for filename (YYYY-MM-DD)
2. Get current time for timestamp (HH:MM:SS)
3. Format user message and assistant reply
4. Append to daily log file

## Use Cases

- **Conversation Backup** - Keep a history of all chats
- **Audit Trail** - Record all interactions for compliance
- **Personal Journal** - Use as a daily conversation journal
- **Debugging** - Review past conversations for troubleshooting

## Requirements

- OpenClaw installed
- Write access to workspace directory
- No external dependencies (uses built-in Node.js modules)

## License

MIT

## Author

Created for OpenClaw community.

---

*This skill is ClawHub-ready and suitable for publishing.*
