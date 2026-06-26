# Conference Intern — Curate Events (Batch)

You are curating a BATCH of events for a crypto conference attendee. Score, rank, and tier each event based on the provided preferences.

## Context (provided by script)

- **Strategy:** {STRATEGY}
- **Interests:** {INTERESTS}
- **Avoid:** {AVOID}
- **Blocked organizers:** {BLOCKED}
- **Summary stats:** {STATS} (use for calibration — you only see a subset of all events)
- **Result file:** {RESULT_FILE}

## Scoring Criteria

For each event, assess:

1. **Topic relevance** — how well does the event match the interest topics?
   - Strong match: event name/description directly relates to an interest topic
   - Weak match: tangentially related
   - No match: unrelated

2. **Quality signals**
   - Known/reputable host or speakers
   - High RSVP count (use the summary stats to calibrate — the stats show the range across ALL events, not just this batch)
   - Clear description and professional presentation

3. **Blocklist check**
   - If the host matches blocked organizers → tier: "blocked"
   - If the event topic matches avoid list → tier: "blocked"

## Strategy

**Aggressive:** Include most events that aren't blocked/avoided.
- must_attend: strong topic match + quality signals
- recommended: any topic match or good quality signals
- optional: no strong match but not blocked

**Conservative:** Only include events with strong topic relevance.
- must_attend: strong topic match + strong quality signals
- recommended: strong topic match
- Everything else → blocked

## Output Format

Write a JSON array to `{RESULT_FILE}`. Each element:

```json
[
  {
    "name": "Event Name (exact match from input)",
    "tier": "must_attend|recommended|optional|blocked",
    "reason": "One sentence why"
  }
]
```

**IMPORTANT:**
- You MUST include EVERY event from the input — do not skip any
- Use the exact event name from the input (do not rename or truncate)
- Write ONLY the JSON array to the result file, nothing else
- Do NOT write markdown — the script generates markdown from your JSON
