---
name: call
description: Call management system with preparation, real-time capture, and follow-up tracking. Use when user mentions phone calls, meetings, conversations, commitments made, or follow-ups needed. Prepares for calls, captures key points and decisions in real-time, tracks action items and commitments, drafts follow-ups, and builds conversation history. All data stored locally.
---

# Call

Call management system. Every conversation, fully leveraged.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All call data stored locally only**: `memory/calls/`
- **No call recording** (unless user explicitly enables separately)
- **No external CRM** connected
- **No sharing** of conversation data
- User controls all data retention and deletion

### Privacy Note
Call records contain sensitive information. All data stays local and private. You control what is captured and retained.

### Data Structure
Call data stored locally:
- `memory/calls/calls.json` - Complete call records
- `memory/calls/contacts.json` - Contact history and context
- `memory/calls/commitments.json` - Commitments made/received
- `memory/calls/followups.json` - Pending follow-ups
- `memory/calls/templates.json` - Follow-up message templates

## Core Workflows

### Prepare for Call
```
User: "I have a call with Acme Corp in 30 minutes"
→ Use scripts/prep_call.py --contact "Acme Corp" --purpose "negotiate contract"
→ Pull previous calls, open commitments, relevant context
```

### Capture During Call
```
User: "Note: They need the proposal by Friday, Sarah is decision maker, follow up on pricing"
→ Use scripts/capture_fragments.py --call-id "CALL-123" --fragments "proposal by Friday, Sarah decision maker, follow up pricing"
→ Build structured notes in real-time
```

### End Call & Generate Summary
```
User: "Call is done"
→ Use scripts/end_call.py --call-id "CALL-123"
→ Generate summary: decisions, action items, commitments
```

### Track Follow-ups
```
User: "What follow-ups do I owe?"
→ Use scripts/check_followups.py
→ Show all pending commitments with deadlines
```

### Draft Follow-up Message
```
User: "Draft follow-up to Sarah"
→ Use scripts/draft_followup.py --contact "Sarah" --call-id "CALL-123"
→ Generate personalized follow-up email with specific references
```

## Module Reference
- **Call Preparation**: See [references/preparation.md](references/preparation.md)
- **Real-time Capture**: See [references/capture.md](references/capture.md)
- **Commitment Tracking**: See [references/commitments.md](references/commitments.md)
- **Follow-up System**: See [references/followups.md](references/followups.md)
- **Conversation History**: See [references/history.md](references/history.md)
- **Contact Intelligence**: See [references/contacts.md](references/contacts.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `prep_call.py` | Prepare for upcoming call |
| `capture_fragments.py` | Capture notes during call |
| `end_call.py` | End call and generate summary |
| `check_followups.py` | Check pending follow-ups |
| `draft_followup.py` | Draft follow-up message |
| `log_call.py` | Log completed call |
| `contact_history.py` | View contact conversation history |
| `commitment_status.py` | Check commitment status |
