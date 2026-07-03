---
name: concierge-wrapper
description: Orchestrate the full Fulcra personal-concierge experience as one seamless flow -- the main entry point that routes to the right sub-skill and runs the morning and evening sequences end to end. Use this whenever the user says things like "start my day", "wrap up my day", "run my concierge", "be my concierge", or gives a request that spans several concierge skills at once. It chains subjective-checkin -> morning-briefing in the morning, and evening-debrief (+ weekly meeting-cadence-optimizer) at night, and routes day-of requests (rate a place, debrief an event, meeting prep) to the right skill. Degrades gracefully when a piece is missing. For a single specific task, the individual skill can be used directly.
---

# Personal Concierge (Orchestration)

The front door to the concierge. It stitches the individual skills into a coherent daily rhythm so the user gets one smooth experience instead of having to know which skill does what. Each sub-skill still works on its own; this wraps them.

## First: check what's available

```bash
uv run --python 3.12 ~/.claude/skills/concierge-wrapper/scripts/status.py
```

Reports which concierge skills are installed, whether Fulcra auth works, and whether Attio is configured. **Use this for graceful degradation:** run what's present, and if something's missing, do the rest and tell the user plainly what was skipped and why ("skipped meeting prep -- Attio isn't connected"). Never abort the whole sequence because one piece is unavailable.

## Morning sequence -- "start my day"

Run as one flowing interaction, not a menu:

1. **subjective-checkin** -- the warm 2-3 question check-in (how they slept/feel). This writes the Morning Check-In annotation.
2. **morning-briefing** -- immediately after, run `collect.py` and deliver the briefing, calibrated to BOTH last night's sleep and what they just told you. Because the check-in ran first, the briefing can open with how they feel, not just the data.

Deliver it as a single continuous experience: the check-in naturally leads into "okay, here's your day." Don't make them ask twice.

## Evening sequence -- "wrap up my day"

1. **evening-debrief** -- the end-of-day reflection (rating, cadence, action items, tomorrow preview). Writes the Evening Debrief annotation.
2. If it's **Sunday or Monday** (or the user asks), also run **meeting-cadence-optimizer** (`analyze`) and fold the insight into the wrap-up: "for the week ahead -- your sweet spot's been ~4 meetings/day."

## Day-of routing (contextual)

When the user surfaces one of these mid-day, route to the matching skill (no need to run a whole sequence):

| The user says... | Route to |
|---|---|
| "rate that place / how was dinner" | **post-experience-rater** |
| "debrief that meeting/event", "log this meeting" | **event-debrief** |
| "who am I seeing / prep me for X / who've I lost touch with" | **relationship-crm** |
| "am I overbooked / meeting cadence" | **meeting-cadence-optimizer** |
| "how am I feeling / journal" | **subjective-checkin** |
| "brief me / what's my day" | **morning-briefing** |

## Weekly rhythm

- **Sunday eve / Monday morning:** meeting-cadence-optimizer, surfaced in the next morning briefing.
- Encourage the daily loop (check-in + debrief) -- the cadence analysis and the taste/relationship graphs only get sharp with consistent use. It's fine to gently note when there isn't enough history yet.

## Graceful degradation -- the rules

- One sub-skill failing or missing never blocks the others. Skip it, name it, continue.
- Each sub-skill is independently usable via its own triggers; the wrapper is a convenience, not a dependency.
- Always be honest about what actually ran and what was stored vs. skipped -- don't imply a briefing happened if the data wasn't there.

## Privacy

This sequence touches the most intimate data the concierge has -- feelings, sleep, calendar, relationships. Never expose specifics in a public/group context. Never print API tokens or secrets.

## Where this fits

The orchestration layer over the whole Fulcra concierge family (shared lib in `~/.fulcra-concierge/lib`): subjective-checkin, morning-briefing, post-experience-rater, evening-debrief, meeting-cadence-optimizer, event-debrief, relationship-crm. (A restaurant-recommender is a planned addition.)
