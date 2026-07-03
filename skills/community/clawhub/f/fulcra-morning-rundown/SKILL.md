---
name: morning-briefing
description: Deliver a personalized morning briefing that combines objective data (last night's sleep, today's calendar, weather) with how the user actually said they feel, and adapts its tone and depth to both. Use this whenever the user says things like "morning briefing", "brief me", "what's my day look like", "what do I have today", or "give me the rundown". Pulls sleep + calendar from Fulcra, the latest subjective check-in, and open action items from the last evening debrief. For capturing how they feel use subjective-checkin; this skill consumes that. For the full "start my day" sequence, the concierge-wrapper runs check-in then this. Do NOT use it for a single objective metric lookup.
---

# Morning Briefing

A briefing calibrated to the human in front of you. Rough night or low mood? Keep it short and gentle. Slept well and feeling sharp? Go deeper on the day. The point is to meet them where they are -- objective data tells you how they slept, the check-in tells you how they *feel*, and the two together set the tone.

This is a lightweight workflow on top of the data the concierge already has. If the official **fulcra-context** / **fulcra-morning-briefing** skills are installed, their richer biometric collectors are great too; this skill reads what it needs directly so it works standalone.

## Prerequisites

- Fulcra CLI authenticated (`uv tool run fulcra-api auth login`).
- Run with `uv run --python 3.12`.

## Step 1 -- Collect context

```bash
uv run --python 3.12 ~/.claude/skills/morning-briefing/scripts/collect.py --location "New+York"
```

(Omit `--location` to skip weather, or set the user's city.) Returns one JSON blob:
- `sleep` -- last night's hours, deep/REM %, quality (poor/fair/good/excellent), or `available:false`
- `calendar` -- today's event count, first start, titles
- `heart_rate` -- recent HR summary (optional)
- `subjective` -- the latest **Morning Check-In** (energy, mood, social battery, intention) if one exists
- `open_loops` -- `action_items` + `open_loops` carried over from the last **Evening Debrief**
- `weather` -- current conditions (via wttr.in)
- `weekday` -- for week-ahead nudges

Any source may be `available:false` -- just skip it; never block the briefing on missing data.

## Step 2 -- Compose, calibrated to BOTH sleep and stated feeling

The magic is adapting to the *combination*. Sleep quality sets the baseline; the subjective check-in overrides it -- if they slept 5 hours but say they feel great, believe them; if they slept 8 but feel low, honor that.

| Their state | Length | Tone | Calendar detail | Suggestions |
|---|---|---|---|---|
| Poor sleep OR low mood/energy | short (~80 words) | gentle, warm, no forced cheer | essentials only | defer non-urgent, protect rest |
| Fair / mixed | medium (~120 words) | practical, steady | key events + a prep tip | pace yourself |
| Good sleep + good energy | full (~160 words) | upbeat, actionable | all events + prep notes | make it count |
| Excellent + high energy | full+ (~180 words) | enthusiastic | all events + opportunities | go big; protect a focus block |

What to weave in:
- **Open with the human:** acknowledge how they feel first, grounded in a number only as a gentle reference ("you got about 6 hours and flagged low energy -- let's keep today light").
- **Calendar:** count, first meeting, anything notable. If energy is low and the day is packed, offer to help triage ("want me to flag what could move?").
- **Open loops:** surface carried-over action items from last night's debrief ("you wanted to send Alex the deck today").
- **Social battery:** if they said low, suggest protecting solo time / making meetings async where possible.
- **Physical notes:** if they flagged something (headache, sore), lighten suggestions accordingly.
- **Weather:** one-line, practical ("52 and rain at 2 -- grab a jacket").

Keep it skimmable. A briefing they actually read beats a complete one they skip.

## Attio meeting context (optional)

If `relationship-crm` is available, you can enrich notable meetings with `prep --name`: *"2pm with Alex -- last time he mentioned Fund III closing."* Don't force it for every event; reserve it for the ones that matter.

## Privacy

Sleep, HR, calendar, and how someone feels are intimate. Never surface specifics in a public/group context -- "they slept well" not "6h2m, 8% deep". Summarize calendar, don't quote sensitive titles. Never print API tokens.

## Where this fits

The synthesis layer of the Fulcra concierge (shared lib in `~/.fulcra-concierge/lib`). It reads **subjective-checkin** (feeling) and **evening-debrief** (open loops) and is the second half of the **concierge-wrapper**'s "start my day" sequence (check-in → briefing). Complements the objective-only official `fulcra-morning-briefing`.
