---
name: crm
version: 1.0.0
description: "Local contact memory and interaction log for operator-reviewed phone follow-up"
metadata: {"amber": {"capabilities": ["read", "act"], "confirmation_required": false, "timeout_ms": 3000, "permissions": {"local_binaries": [], "telegram": false, "openclaw_action": false, "network": false}, "function_schema": {"name": "crm", "description": "Manage local contacts and interaction history for operator-reviewed phone follow-up. Use lookup_contact at the start of inbound calls (automatic, using caller ID) to check if the caller is known and retrieve relevant operator-approved context. Use upsert_contact to save caller-volunteered contact details (name, email, company) when appropriate under the operator's caller notice/consent policy. Use log_interaction at the end of every call to record what happened (summary, outcome). Use context_notes for concise, relevant follow-up context; avoid sensitive, intimate, or unnecessary personal details. Do not ask robotic CRM questions; capture only details naturally relevant to the call purpose and retention policy.", "parameters": {"type": "object", "properties": {"action": {"type": "string", "enum": ["lookup_contact", "upsert_contact", "log_interaction", "get_history", "search_contacts", "tag_contact"], "description": "The CRM action to perform"}, "phone": {"type": "string", "description": "Contact phone number in E.164 format (e.g. +14165551234)", "pattern": "^\\+[1-9]\\d{6,14}$|^$"}, "name": {"type": "string", "maxLength": 200}, "email": {"type": "string", "maxLength": 200}, "company": {"type": "string", "maxLength": 200}, "context_notes": {"type": "string", "maxLength": 1000, "description": "Concise operator-reviewed follow-up context. Avoid sensitive, intimate, or unnecessary personal details."}, "summary": {"type": "string", "maxLength": 500, "description": "One-liner: what the call was about"}, "outcome": {"type": "string", "enum": ["message_left", "appointment_booked", "info_provided", "callback_requested", "transferred", "other"], "description": "Call outcome"}, "details": {"type": "object", "description": "Structured extras as key-value pairs (e.g. appointment_date, purpose)"}, "query": {"type": "string", "maxLength": 200}, "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10}, "add": {"type": "array", "items": {"type": "string", "maxLength": 50}, "maxItems": 10}, "remove": {"type": "array", "items": {"type": "string", "maxLength": 50}, "maxItems": 10}}, "required": ["action"]}}}}
---

# CRM Skill — Contact Memory for Voice Calls

Stores local, operator-reviewed caller context and interaction history for phone follow-up.

## How It Works

### On Every Inbound Call

1. **Lookup** — Call `crm` with `lookup_contact` using the caller's phone number (from Twilio caller ID).
2. **If known** — Greet by name and use `context_notes` to personalize (ask about their dog, remember their preference, etc.)
3. **If unknown** — Proceed normally, listen for their name.

### During the Call

When someone shares their name, email, company, or relevant follow-up details, upsert it via `crm.upsert_contact` only if that fits the operator's caller notice/consent and retention policy. Avoid collecting sensitive or unnecessary personal details.

### At End of Call

1. Log the interaction: `log_interaction` with summary + outcome
2. Update context_notes with concise, relevant follow-up context, synthesizing with what was known before

### On Outbound Calls

Same exact flow: lookup at start, upsert + log_interaction at end.

## API Reference

| Action | Purpose |
|--------|---------|
| `lookup_contact` | Fetch contact + last 5 interactions + context_notes. Returns null if not found. |
| `upsert_contact` | Create or update a contact by phone. Only provided fields are updated. |
| `log_interaction` | Log a call: summary, outcome, details. Auto-creates contact if needed. |
| `get_history` | Get past interactions for a contact (sorted newest-first). |
| `search_contacts` | Search by name, email, company, notes. |
| `tag_contact` | Add/remove tags (e.g. "vip", "callback_later"). |

## Privacy

- **Event details stay private.** Like the calendar skill, never disclose event details to callers.
- **CRM context is personal.** The `context_notes` field is for Amber's internal memory, not for sharing call transcripts. Use it to inform conversation, not to recite it.
- **PII storage.** Phone, name, email, company, context_notes, call summaries, and interaction metadata are stored locally in SQLite. Operators must provide appropriate caller notice/consent and retention/deletion practices. No network transmission, no external CRM by default.
- **Review and correction.** Operators should periodically review, correct, or delete CRM entries so inaccurate transcript extraction or overly sensitive details do not persist.

## Security

- Synchronous SQLite (better-sqlite3) with parameterized queries — no SQL injection surface
- Private number detection — calls from anonymous/blocked numbers are skipped entirely
- Input validation at three levels: schema patterns, handler validation, database constraints
- Database file created with mode 0600 (owner read/write only)

## Examples

**Greeting a known caller:**
```
Amber: "Hi Sarah, good to hear from you again. How's Max doing?" 
[context_notes remembered: "Has a Golden Retriever named Max. Prefers afternoon calls."]
```

**Capturing relevant follow-up context:**
```
Caller: "By the way, I got married last month!"
Amber: [only records this if it is relevant and appropriate under the operator's retention policy]
Amber (aloud): "That's wonderful! Congrats!"
```

**End-of-call log:**
```
Amber: [calls log_interaction: summary="Called to reschedule Friday appointment", outcome="appointment_booked"]
Amber: [calls upsert_contact with context_notes: "Prefers afternoon callbacks. Usually calls to reschedule appointments."]
```
