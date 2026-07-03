---
name: evening-debrief
description: Run a short end-of-day debrief that reflects on how the day went, extracts action items and open loops, and previews tomorrow -- then store it in Fulcra as a structured annotation. Use this whenever the user says things like "evening debrief", "wrap up my day", "end of day", "how was my day", "let's debrief", or signals they're winding down and want to reflect. Reads today's and tomorrow's calendar and this morning's check-in for context. For a single specific event (with attendees + follow-ups) use event-debrief instead; for the morning version use subjective-checkin. Do NOT use it for objective health/calendar data pulls.
---

# Evening Debrief

A 3-5 minute end-of-day reflection: summarize the day, capture how it felt, pull out the loose threads, and look at tomorrow so the user can put the day down. Reflective but light -- a smart coach who remembers everything, not a heavy journaling chore.

## Prerequisites

- Fulcra CLI authenticated (`uv tool run fulcra-api auth login`).
- Run with `uv run --python 3.12`.

## Step 1 -- Gather context

```bash
uv run --python 3.12 ~/.claude/skills/evening-debrief/scripts/evening_debrief.py context
```

Returns: today's calendar (count + titles), tomorrow's calendar (count + first start), and this morning's `subjective-checkin` if one exists (so you can compare planned energy to how the day actually went). Any piece may be `available:false` -- proceed without it; never block the debrief on missing data.

Open with a grounded summary from this, e.g. *"You had 6 things on the calendar today, and your morning energy was a 7. How did it actually go?"*

## Step 2 -- The reflection

Keep it conversational. Cover roughly:

1. "How would you rate today, 1-10?"
2. "You had [N] meetings -- was that too many, about right, or too few?" (capture a preferred cap if they volunteer one)
3. "When did your energy peak or dip?"
4. If the rating is < 8: "What would've made today a [rating+2]?"
5. "Any wins worth naming?" and "Anything still open -- follow-ups, loose threads?"

Listen for commitments and turn them into action items (action + deadline + a little context). If they mention a person to follow up with, note it -- you can offer to hand off to relationship-crm/event-debrief afterward.

## Step 3 -- Save

Assemble the JSON and run `save`. A quick `--dry-run` to show what you captured is a nice touch but optional.

```bash
uv run --python 3.12 ~/.claude/skills/evening-debrief/scripts/evening_debrief.py save --payload /tmp/debrief.json
```

### Payload schema

```json
{
  "date": "2026-05-29",
  "day_rating": 7,
  "meeting_count": 6,
  "meeting_cadence_feedback": "too many",
  "preferred_meeting_cap": 4,
  "energy_trajectory": "started at 7, dipped to 4 by 3pm",
  "improvement_note": "fewer back-to-back calls in the afternoon",
  "action_items": [{"action": "Send Alex the deck", "deadline": "tomorrow", "context": "afternoon mtg"}],
  "tomorrow_meeting_count": 4,
  "open_loops": ["Alex birthday planning"],
  "wins": ["shipped the proposal"]
}
```

Fill what you gathered; omit the rest. `day_rating`, `meeting_count`, and `meeting_cadence_feedback` are the fields the **meeting-cadence-optimizer** later correlates against energy/mood -- capture them when you can, since they're what make the weekly pattern analysis possible.

## What `save` does

Writes one "Evening Debrief" moment annotation (created once, reused) carrying the structured reflection, and reports `verified_matches`. Only claim success when `ok` is true / `verified_matches >= 1`.

## After saving

Close warmly: reflect today's rating, the top 1-2 action items with deadlines, and tomorrow's load ("4 meetings, first at 9"). If anything is time-sensitive for tomorrow morning, flag it. Offer (don't push) to add reminders or hand follow-ups to the relationship skills.

## Privacy

Day ratings, energy, and what's on the calendar are personal. Don't surface them publicly. Never print API tokens.

## Where this fits

Part of the Fulcra personal concierge family (shared lib in `~/.fulcra-concierge/lib`). It reads **subjective-checkin** (morning energy) to bookend the day, and its `day_rating`/`meeting_count` records are the primary input to **meeting-cadence-optimizer**. For deep single-event capture, it hands off to **event-debrief**.
