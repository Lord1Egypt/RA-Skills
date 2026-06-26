# Draft Router Skill

Route incoming drafts via Telegram inline buttons. Forwards messages get three action options.

## Installation

```bash
# Make executable
chmod +x /home/node/.openclaw/workspace/skills/draft-router/draft-router.js
```

## Usage

Auto-detects drafts by header pattern: `DRAFTS | YYYY-MM-DD HH:MM ---`

```javascript
// From an OpenClaw agent
const router = require('./skills/draft-router/draft-router.js');

// Check if message is a draft
if (router.isDraftMessage(messageText)) {
  const result = router.handleDraft(messageText, 'drafts-app');
  
  // Send via Telegram with buttons
  message.send({
    to: chatId,
    message: result.text,
    buttons: result.buttons
  });
}
```

## Button Actions

| Button | Action |
|--------|--------|
| 🧠 Knowledge | Appends to MEMORY.md with timestamp and source |
| 📦 Archive | Saves to `memory/drafts-archive/archived/` |
| ✅ Tasks | Adds to SESSION-STATE.md as an active task |
| ▶️ Run as Prompt | Prepares for execution; asks qualifying questions one at a time |

## File Structure

```
workspace/
├── skills/draft-router/
│   ├── SKILL.md
│   └── draft-router.js
└── memory/
    └── drafts-archive/
        ├── archived/       # Archived drafts
        ├── prompts/        # Drafts marked for prompt execution
        └── processed/      # Knowledge additions
```

## Callback Handling

Callbacks use format: `draft:{id}:{action}`

```javascript
// Parse callback
callback_data.split(':') // ['draft', 'id', 'action']

// Execute
const result = router.handleCallback(draftId, action);
```

## Integration with AGENTS.md

Add to your agent's routing logic:

```javascript
// When message is forwarded or has draft content
if (isForwarded || message.text.includes('#draft')) {
  const router = require('../skills/draft-router/draft-router.js');
  const result = router.handleDraft(message.text, message.from);
  
  return {
    message: result.text,
    buttons: result.buttons
  };
}
```
