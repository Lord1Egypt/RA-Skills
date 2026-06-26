---
name: claw-chat
description: Claw Chat AI messaging assistant. Use when the user wants to enhance conversations in Claw Chat, manage message threads, draft smart replies, summarize chat history, or set up AI-assisted communication workflows. Triggers on "Claw Chat", "clawchat", "chat assistant", "message summary", "smart reply", or "AI messaging".
---

# Claw Chat Skill

Claw Chat is an AI-native messaging platform where every conversation is enhanced by intelligent assistance. This skill helps you communicate more effectively, stay on top of important threads, and never miss what matters.

## Capabilities

- **Smart replies**: Draft context-aware responses for any message
- **Thread summaries**: Catch up on long conversations instantly
- **Message drafting**: Write clear, professional, or casual messages in your voice
- **Priority filtering**: Identify which messages need your attention now
- **Follow-up tracking**: Never let important replies fall through the cracks
- **Tone adjustment**: Shift message tone from casual to formal (or vice versa)

## Common Tasks

- "Summarize this conversation thread"
- "Draft a reply to this message"
- "Make this message sound more professional"
- "What are the action items from this chat?"
- "Remind me to follow up on this conversation tomorrow"

## Smart Reply Framework

```
Acknowledge → Answer → Action

Example incoming: "Hey, can we push the Monday meeting to Wednesday?"

Smart reply options:
  Casual:      "Wednesday works for me! Morning or afternoon?"
  Formal:      "Wednesday works. Could you confirm a specific time?"
  Detailed:    "Wednesday works. I'm available 10am-12pm or after 3pm — 
                which slot works better for you?"
```

## Message Tone Guide

```
Too casual → More professional:
  "yeah sure" → "Sounds good, I'll take care of it."
  "idk" → "I'm not certain — let me look into it and get back to you."

Too formal → More human:
  "I acknowledge receipt of your inquiry" → "Got it, thanks!"
  "Please be advised that" → "Just so you know,"

Assertive without aggressive:
  Add: "I think", "In my view", "From my perspective"
  Soften: "Would it be possible to..." instead of "You need to..."
```

## Conversation Summary Template

```
📋 Thread: [Topic]
👥 Participants: [Names]
📅 Date range: [From - To]

🔑 Key points:
  • [Main discussion point 1]
  • [Main discussion point 2]

✅ Decisions made:
  • [Decision 1]

📌 Action items:
  • [Person] → [Task] by [deadline]

❓ Open questions:
  • [Unresolved item]
```

## Follow-up System

```
Trigger phrases to watch for:
  "I'll get back to you on..."
  "Let me check and..."
  "We should discuss..."
  "Circle back next week"

Auto-create follow-up when:
  → You send a message with a question and get no reply in 48h
  → You agree to do something ("I'll send it by Friday")
  → Someone promises a deliverable
```

## Tips

- Use **@mentions** to ensure the right person sees your message
- Keep threads **focused** — one topic per thread reduces confusion
- Use **reactions** to acknowledge messages without adding noise
- Set **message reminders** for anything you need to act on later
- Claw Chat's AI can **auto-tag** messages by project, priority, or topic
