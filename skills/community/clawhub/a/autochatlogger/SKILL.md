# activity_logger 📝

A minimal skill for logging conversation messages to daily Markdown files.

## Purpose

Automatically log every user message and assistant reply to a daily Markdown file.

## What It Does

- Creates one log file per day: `workspace/chat/YYYY-MM-DD.md`
- Appends each conversation entry to the daily file
- Never overwrites existing data
- Creates directories and files automatically if they don't exist

## Log Format

```markdown
[HH:MM:SS]
User: <message>
Assistant: <reply>
```

## How It Works

The agent should manually log each conversation turn using this logic:

### 1. Create Daily Log File

```javascript
const fs = require('fs');
const path = require('path');
const os = require('os');

// Get workspace path
const workspace = process.cwd(); // or your workspace path
const chatDir = path.join(workspace, 'chat');

// Create directory if it doesn't exist
if (!fs.existsSync(chatDir)) {
  fs.mkdirSync(chatDir, { recursive: true });
}

// Get current date for filename
const now = new Date();
const dateStr = now.toISOString().split('T')[0]; // YYYY-MM-DD
const timeStr = now.toTimeString().split(' ')[0]; // HH:MM:SS

const logFile = path.join(chatDir, `${dateStr}.md`);
```

### 2. Append Log Entry

```javascript
// Format log entry
const userMsg = /* get user message */;
const assistantMsg = /* get assistant reply */;

let logEntry = `\n[${timeStr}]\n`;
if (userMsg) {
  logEntry += `User: ${userMsg}\n`;
}
if (assistantMsg) {
  logEntry += `Assistant: ${assistantMsg}\n`;
}

// Append to file
fs.appendFileSync(logFile, logEntry);
```

### 3. Example Entry

```markdown
[14:30:00]
User: Hello, how are you?
Assistant: I'm doing well, thank you for asking!

[14:32:15]
User: What's the weather like today?
Assistant: Let me check the weather for you.
```

## Log Location

```
workspace/chat/YYYY-MM-DD.md
```

Example:
```
C:\Users\user\OpenClawWorkspace\chat\2026-03-07.md
```

## Usage Notes

- This is a **manual logging skill** - the agent writes to the log file after each response
- The skill doesn't use hooks - it's triggered by agent code
- Each entry is appended with a timestamp
- The file is created automatically on first entry of the day
- Multiple conversations on the same day go to the same file

## Integration

To use this skill:

1. Copy the `chat/` directory structure to your workspace
2. After each agent response, append the user message and assistant reply to the daily log file
3. Use the format shown above

## Files

- `SKILL.md` - This file
- `README.md` - ClawHub package readme

## License

MIT
