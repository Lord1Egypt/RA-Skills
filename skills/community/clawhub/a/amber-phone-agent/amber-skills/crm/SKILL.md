---
name: crm
version: 1.0.0
description: "Local contact memory and interaction log for operator-reviewed phone follow-up"
metadata: {"amber": {"capabilities": ["read", "act"], "confirmation_required": false, "timeout_ms": 3000, "permissions": {"local_binaries": [], "telegram": false, "openclaw_action": false, "network": false}, "function_schema": {"name": "crm", "description": "Manage local CRM for the phone number tied to this call. Use lookup_contact for relevant operator-approved context, upsert_contact for caller-volunteered details when appropriate under the operator’s notice and consent policy, and log_interaction for relevant follow-up. Keep notes concise and avoid sensitive or unnecessary personal details. Use the operator MCP CRM tools to search or manage other contacts.", "parameters": {"type": "object", "properties": {"action": {"type": "string", "enum": ["lookup_contact", "upsert_contact", "log_interaction", "get_history", "tag_contact"], "description": "The CRM action to perform"}, "phone": {"type": "string", "description": "Optional. Amber uses the number tied to this call. If supplied, this number must match.", "pattern": "^\\+[1-9]\\d{6,14}$|^$"}, "name": {"type": "string", "maxLength": 200}, "email": {"type": "string", "maxLength": 200}, "company": {"type": "string", "maxLength": 200}, "context_notes": {"type": "string", "maxLength": 1000, "description": "Concise operator-reviewed follow-up context. Avoid sensitive, intimate, or unnecessary personal details."}, "summary": {"type": "string", "maxLength": 500, "description": "One-liner: what the call was about"}, "outcome": {"type": "string", "enum": ["message_left", "appointment_booked", "info_provided", "callback_requested", "transferred", "other"], "description": "Call outcome"}, "details": {"type": "object", "description": "Structured extras as key-value pairs (e.g. appointment_date, purpose)"}, "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10}, "add": {"type": "array", "items": {"type": "string", "maxLength": 50}, "maxItems": 10}, "remove": {"type": "array", "items": {"type": "string", "maxLength": 50}, "maxItems": 10}}, "required": ["action"]}}}}
---

# CRM Skill — Contact Memory for Voice Calls

Stores local, operator-reviewed caller context and interaction history for phone follow-up.

## How It Works

### On Every Inbound Call

1. **Lookup** — Call `crm` with `lookup_contact` using the caller's phone number (from Twilio caller ID) only under the operator's caller notice/consent and retention policy.
2. **If known** — Greet by name and use `context_notes` only when relevant to the call purpose. Avoid surprising rapport-building from intimate or unnecessary details.
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
Amber: "Hi Sarah, good to hear from you again. I have you down as preferring afternoon callbacks."
[context_notes remembered: "Prefers afternoon callbacks for appointment changes."]
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
