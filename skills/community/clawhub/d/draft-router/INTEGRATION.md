# Draft Router - Auto-Detection for Telegram

## How It Works

Detects draft messages by header pattern: `DRAFTS | YYYY-MM-DD HH:MM ---`

This format is used by the Drafts app script when sending messages to Telegram.

## Integration

Add this logic to your agent's message handler (AGENTS.md or session handling):

```javascript
const router = require('./skills/draft-router/draft-router.js');

// Check if message matches draft pattern
if (router.isDraftMessage(messageText)) {
  const result = router.handleDraft(messageText, 'drafts-app');
  
  // Reply with buttons
  return {
    message: result.text,
    buttons: result.buttons
  };
}
```

## Callback Handling

When a button is clicked, the callback data arrives as a new message starting with `draft:`

Parse and route:

```javascript
if (messageText.startsWith('draft:')) {
  const parts = messageText.split(':');
  const draftId = parts[1];
  const action = parts[2];
  
  const router = require('./skills/draft-router/draft-router.js');
  const result = router.handleCallback(draftId, action);
  
  if (result.error) {
    return { message: `❌ ${result.error}` };
  }
  
  // Handle the action result
  switch (result.action) {
    case 'knowledge':
      return { message: result.message }; // ✅ Added to MEMORY.md
      
    case 'archive':
      return { message: result.message }; // ✅ Archived
      
    case 'tasks':
      return { message: result.message }; // ✅ Added to SESSION-STATE.md as task
      
    case 'prompt':
      // Start prompt mode - ask first qualifying question
      return { 
        message: `${result.message}\n\n---\n\n${result.content}\n\nWhat would you like me to do with this? (Ask your first question)`
      };
  }
}
```

## File Locations

- Draft router: `workspace/skills/draft-router/draft-router.js`
- Archive: `workspace/memory/drafts-archive/`
- Knowledge: `workspace/MEMORY.md`

## Testing

Send a message with the draft header format:

```
DRAFTS | 2026-02-18 18:49
---
Your draft content here...
```

You should see:

```
📄 Draft received
Preview: Your draft content here...
What would you like to do?
[🧠 Knowledge] [📦 Archive] [✅ Tasks]
[▶️ Run as Prompt]
```
