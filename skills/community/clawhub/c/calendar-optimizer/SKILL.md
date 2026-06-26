---
name: calendar-optimizer
description: Analyzes and rewrites calendar events into clear, actionable tasks. Removes meeting fluff and converts vague descriptions into specific deliverables with deadlines.
metadata:
  openclaw:
    emoji: "📅"
    requires:
      bins: [python3]
    always: false
---

# Calendar Optimizer

Transforms messy calendar events into clear, actionable tasks.

## Usage

```bash
python3 optimize.py --input calendar.csv --output tasks.md
```

## Input Format

```csv
event,time,attendees
"Synergy sync - let's circle back",Monday 2pm,5
"Q4 Planning - moving forward paradigm shift",Tuesday 10am,8
```

## Output

```markdown
## Monday 2pm — Synergy Sync
**Actual topic:** Website redesign review
**Action:** Review mockups and give feedback
**Prep:** Bring 3 specific comments
**Attendees:** 5 (note: consider sending deputy)

## Tuesday 10am — Q4 Planning
**Actual topic:** Q4 OKR finalization
**Action:** Approve final OKRs
**Prep:** Review draft OKRs sent Friday
**Attendees:** 8 (decision-maker: Sarah)
```
