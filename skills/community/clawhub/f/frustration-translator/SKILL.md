---
name: frustration-translator
description: Detect user frustration in prompts and translate charged/emotional language into clear, actionable instructions. Use when user messages contain vague anger ("this is garbage"), compressed expectations ("just fix it"), repeated complaints about the same issue, ALL CAPS, or emotional language that obscures what they actually need done. Critical for finite context windows where misinterpreting a frustrated prompt wastes tokens on the wrong task. Improves over time by logging frustration patterns and their resolved meanings.
---

# Frustration Translator

Detect emotional charge → extract the real instruction → execute what they meant.

## Score (0–10)

| Signal | Points |
|--------|--------|
| Vague blame ("this is broken") | +3 |
| Compressed expect ("just fix it") | +2 |
| Wasted resources ("burned $75") | +3 |
| Contrast with past ("yesterday it worked") | +2 |
| CAPS / excessive punctuation | +1 |
| Repeated topic 3x+ | +2 |
| Short after long messages | +2 |

**0–3**: Normal. **4–6**: Translate first. **7–10**: Brief ack, translate, execute fast.

## Translation

| They say | They mean | Find it by |
|----------|-----------|------------|
| "This is broken" | Specific thing failed | Check last 2–3 messages |
| "Just fix it" | Already explained, don't repeat | Re-read earlier explanation |
| "Do it right this time" | Previous attempt had specific flaw | Find the flaw |

## Response Pattern
Brief ack → show you got the real problem → start fixing → show evidence.

```
❌ "I apologize for the issues. Let me analyze what went wrong..."
✅ "Yeah, bad day. The issue was [X]. Fixing now."
```

## Rules
- Never psychoanalyze or ask "are you frustrated?"
- Never slow down when they want speed — frustration = urgency.
- Never add caveats when they want action.
- Not every short message is frustrated — some people are concise.
