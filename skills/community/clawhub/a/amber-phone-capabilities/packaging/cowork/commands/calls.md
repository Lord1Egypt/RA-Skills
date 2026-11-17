---
name: calls
description: View recent call history, transcripts, and summaries
arguments:
  - name: filter
    description: "all", "inbound", "outbound", or "missed" (default: all)
    required: false
  - name: limit
    description: Number of recent calls to show (default: 10)
    required: false
---

# /amber:calls

View your recent call history with transcripts and AI-generated summaries.

Call history contains sensitive communications data, including phone numbers, summaries, and transcripts. Only run this in a trusted local workspace and follow your retention/deletion policy.

## Usage

```
/amber:calls
/amber:calls inbound
/amber:calls outbound 5
```

## Output

For each call, shows:
- Direction (inbound/outbound)
- Caller/recipient name and number
- Date and duration
- AI summary of the conversation
- Full transcript (expandable)
