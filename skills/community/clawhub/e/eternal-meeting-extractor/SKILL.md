---
name: meeting-extractor
description: Extract action items, decisions, and key points from meeting transcripts or notes. Use when the user has meeting notes, call transcripts, or recorded meeting text and wants: action items extracted, decisions highlighted, summary generated, or follow-up tasks identified. Triggers on "summarize meeting", "extract action items", "meeting notes", "what were the decisions", "meeting recap".
---

# Meeting Extractor

Parse meeting transcripts into structured summaries with action items.

## Usage

```bash
python3 scripts/meeting.py extract transcript.txt
python3 scripts/meeting.py extract --format json transcript.txt
python3 scripts/meeting.py extract --followup transcript.txt
```

## What It Extracts

- **Summary** — 3-5 sentence overview
- **Decisions** — Agreed-upon choices
- **Action Items** — Tasks with owners and deadlines
- **Key Points** — Important discussion topics
- **Questions** — Unresolved questions needing answers
- **Attendees** — Who participated

## Output Formats

- Text (default) — Human-readable summary
- JSON — Machine-readable for task systems
- Markdown — For documentation/wiki
