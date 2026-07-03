---
name: post-experience-rater
description: Capture a fast, casual rating right after the user finishes something -- a restaurant, hotel, trip, event, or meeting a new person -- and store it in Fulcra as a structured annotation that builds their long-term taste/preference graph. Use this whenever the user says things like "rate that restaurant", "how was dinner", "log a rating", "rate the hotel", "that place was a 4", or otherwise reacts to an experience they just had. Keep it to ~15 seconds, like texting a friend. For a deeper per-event capture with attendees and follow-ups use event-debrief; for a whole-day wrap-up use evening-debrief. Do NOT use it for objective health/calendar data pulls.
---

# Post-Experience Rater

A 15-second micro check-in after an experience. The point is speed and low friction -- this should feel like texting a friend "how was it?", not filling out a form. Each rating becomes a Fulcra annotation that, over time, builds the user's taste graph (what a future restaurant recommender and other skills draw on).

## Prerequisites

- Fulcra CLI authenticated (`uv tool run fulcra-api auth login`).
- Run with `uv run --python 3.12`.

## The conversation (keep it fast)

1. "How was [place/experience]?"
2. If it's a restaurant: "Food, vibe, service -- quick 1-5 each?" (For a hotel, use room/location/service; for an event, just an overall score is fine. Use whatever 1-5 keys fit.)
3. "Would you go back?"
4. "Anything worth remembering?" -- one free-text line ("too loud for a date night", "the pasta was incredible, bar seats are better").

Infer tags (cuisine, neighborhood, occasion) and companions from what they say; don't interrogate. Two or three quick exchanges is the whole thing.

## Save

Assemble a small JSON file and run `save`. `--dry-run` first if you want to show the user what's being stored; for this skill it's fine to save directly once you've reflected their answer back, since it's low-stakes and fast.

```bash
uv run --python 3.12 ~/.claude/skills/post-experience-rater/scripts/post_experience.py save --payload /tmp/rating.json
```

### Payload schema

```json
{
  "experience_type": "restaurant",
  "name": "Carbone",
  "scores": {"food": 5, "vibe": 4, "service": 3},
  "would_return": true,
  "notes": "Too loud for a date night but the pasta was incredible. Bar seats are better.",
  "companions": ["Jordan"],
  "tags": ["italian", "west village", "special occasion"]
}
```

Only `name` is strictly required. `scores` accepts any 1-5 keys appropriate to the experience type. Fill what the user gave you; don't invent scores they didn't state.

## What `save` does

Writes one "Post-Experience Rating" moment annotation (created once, reused after) carrying the full JSON, and reports `verified_matches`. Only report success when `ok` is true / `verified_matches >= 1` -- not from a bare HTTP code.

## After saving

Reflect it back in one warm line ("Got it -- Carbone, 5/4/3, you'd go back, too loud for dates. Logged."). That's it. If they mentioned a noteworthy new person, you can offer to add them via the relationship-crm/event-debrief skills -- but don't push.

## Privacy

Ratings and companions are personal. Don't surface them in a public/group context. Never print API tokens.

## Where this fits

Part of the Fulcra personal concierge family (shared lib in `~/.fulcra-concierge/lib`). These ratings are the raw material for a future **restaurant-recommender** and feed the preference signal that **meeting-cadence-optimizer** and **evening-debrief** complement on the time/energy side.
