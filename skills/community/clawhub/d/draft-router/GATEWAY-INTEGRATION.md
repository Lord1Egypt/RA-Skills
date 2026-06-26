# Gateway Integration for Draft Router

## Overview

This document specifies how to integrate the draft-router skill into OpenClaw's gateway for automatic draft detection on incoming Telegram messages.

## Current Flow

```
Telegram Webhook → Gateway → Session Router → Agent Session
```

## Desired Flow

```
Telegram Webhook → Gateway → Draft Detector? 
                                   ↓
                              YES: Send buttons directly
                                   ↓
                               NO: Route to Session
```

## Integration Points

### 1. Telegram Channel Handler (Pre-Routing)

Location: OpenClaw gateway's telegram channel handler

Add draft detection before session creation:

```typescript
// In packages/gateway/src/channels/telegram/handler.ts
// Or equivalent telegram message processing

import { isDraftMessage, handleDraft } from '../../../../../workspace/skills/draft-router/draft-router.js';

async function processTelegramMessage(update: TelegramUpdate) {
  const messageText = update.message?.text || update.message?.caption;
  
  // Check if this is a draft message
  if (messageText && isDraftMessage(messageText)) {
    const router = require('../../../../../workspace/skills/draft-router/draft-router.js');
    const result = router.handleDraft(messageText, 'telegram-drafts-app');
    
    // Send inline buttons directly via Telegram API
    await telegramBot.sendMessage({
      chat_id: update.message.chat.id,
      text: result.text,
      reply_markup: {
        inline_keyboard: result.buttons
      }
    });
    
    // Store draft for callback handling
    // The draft-router.js already stores it in memory/drafts-archive/
    
    return; // Skip normal session routing
  }
  
  // Continue to normal session routing
  return routeToSession(update);
}
```

### 2. Callback Query Handler

Handle button clicks (callback queries):

```typescript
// In telegram callback query handler

async function processCallbackQuery(callbackQuery: CallbackQuery) {
  const data = callbackQuery.data;
  
  if (data?.startsWith('draft:')) {
    const [, draftId, action] = data.split(':');
    const router = require('../../../../../workspace/skills/draft-router/draft-router.js');
    const result = router.handleCallback(draftId, action);
    
    if (result.error) {
      await telegramBot.answerCallbackQuery({
        callback_query_id: callbackQuery.id,
        text: result.error
      });
      return;
    }
    
    // Send result message
    await telegramBot.sendMessage({
      chat_id: callbackQuery.message.chat.id,
      text: result.message
    });
    
    // Answer the callback (removes loading state)
    await telegramBot.answerCallbackQuery({
      callback_query_id: callbackQuery.id
    });
    
    // For 'prompt' action, create a session to continue
    if (result.action === 'prompt') {
      // Create agent session with the draft content as context
      await createSession({
        agentId: 'main',
        context: `Draft to process: ${result.content}`,
        initialMessage: 'Running this draft as a prompt. What would you like me to do?'
      });
    }
    
    return;
  }
  
  // Continue with other callback handling
}
```

### 3. Alternative: Webhook Middleware

If modifying the core handler is complex, use middleware:

```typescript
// middleware/draft-detector.ts

export async function draftDetectorMiddleware(req, res, next) {
  // Only process Telegram webhooks
  if (req.path !== '/webhook/telegram') {
    return next();
  }
  
  const update = req.body;
  const messageText = update.message?.text;
  
  if (messageText && isDraftMessage(messageText)) {
    // Handle as draft - don't call next()
    const result = handleDraft(messageText, 'telegram');
    
    // Send response directly
    await sendTelegramButtons(update.message.chat.id, result);
    
    res.status(200).send('OK');
    return;
  }
  
  // Not a draft - continue to normal routing
  next();
}
```

## Files to Modify

1. **Gateway telegram handler** (`packages/gateway/src/channels/telegram/`)
   - Add draft detection in message processing
   - Add callback query handling for `draft:*` patterns

2. **Skill registration** (optional)
   - Register draft-router as a gateway-level skill
   - Add to `config.skills.entries` in openclaw.json

## Testing

After integration, test with:

```
DRAFTS | 2026-02-18 20:00
---
Test draft content here
```

Expected: Buttons appear immediately without agent session created.

## Notes

- The draft-router.js skill must be accessible from the gateway context
- Ensure proper error handling for missing draft files
- Consider rate limiting for draft processing
- The gateway must have filesystem access to `workspace/memory/drafts-archive/`
