# Event suitability rubric

For calendar-driven invocations (the agent reads a customer's calendar and decides whether to proactively build a lookbook for an event), score the event 0–10 on "would this customer benefit from a wardrobe-aware lookbook?" Only events scoring ≥ **6** trigger a lookbook generation; everything below scores doesn't.

The agent never generates a lookbook for events it shouldn't (medical appointments, work syncs, errands) — that's how trust is kept on the calendar-integration channel.

## The rubric (0–10)

```
score = type_weight + dress_code_weight + duration_weight + location_weight + customer_signal
```

### type_weight (0–4)

| Event class | Weight | Examples |
|---|---|---|
| Wedding / engagement / formal | 4 | "Sarah & Tom's wedding", "Black-tie gala", "Bar mitzvah" |
| Travel (multi-day) | 3 | "SF trip Mar 14–18", "Paris vacation", "Sonoma weekend" |
| Concert / show / nightlife | 2 | "Tycho at Greek", "dinner + show", "speakeasy" |
| Party / dinner / social | 2 | "Friend's birthday", "Friday dinner with [name]" |
| Conference / professional headshot / on-stage | 2 | "Stripe Sessions", "podcast taping", "panel" |
| Meeting / one-on-one / casual lunch | 0 | "1:1 with Alex", "coffee w/ J" |
| Errand / appointment / admin | 0 | "Costco run", "DMV", "dry cleaner" |
| Medical / dental / therapy / mental health | -10 | "Dr. Lee", "annual physical", "therapy" |
| Childcare / family logistics | 0 | "School pickup", "Soccer practice" |
| Reminder / TODO / no-context block | 0 | "Block: focus", "Reminder: pay bills" |

A `-10` weight is a hard veto — the agent never builds a lookbook for medical or therapy appointments, regardless of other signals. This is one of the trust-preserving rules; getting this wrong feels invasive.

### dress_code_weight (0–3)

Inferred from the event description if explicit, otherwise from the type:

| Cue | Weight |
|---|---|
| Explicit dress code in the event ("smart casual", "black tie", "creative", "festive attire") | +3 |
| Venue implies a code ("dinner at Bestia", "speakeasy", "the Standard rooftop") | +2 |
| Outdoor / vacation / travel where wardrobe matters | +2 |
| No dress-code cue, casual default | 0 |

### duration_weight (0–1)

| Duration | Weight |
|---|---|
| Multi-day (2+ nights) | +1 |
| Single-evening / single-day | 0 |

Multi-day trips need a capsule, not a single outfit — that earns the lookbook a small bonus regardless of formality.

### location_weight (0–1)

| Location | Weight |
|---|---|
| Travel destination ≠ customer's home metro | +1 |
| Local | 0 |

Different climate / dress norms = harder to plan → lookbook value-add.

### customer_signal (-2 to +2)

Reads the customer's chat history (or `profile.md → notes`) for explicit ask:

| Signal | Weight |
|---|---|
| Customer asked to be reminded ("set me up for Sonoma weekend") | +2 |
| Customer mentioned the event positively to the agent before | +1 |
| Customer told the agent to skip lookbook prompts on this event class | -2 |

## Score → action

| Score | Action |
|---|---|
| ≤ 5 | Skip silently. Don't surface anything. |
| 6 | Soft surface — one sentence on the next interactive turn ("you have X coming up — want a lookbook?"). Never auto-generate. |
| 7–8 | Auto-generate the **Editorial tier** **locally** (no try-on; product imagery + flat-lays). Saves the OpenAI cost; customer can request the premium tier if they want try-on. |
| 9–10 | Auto-generate the **Premium tier** **locally**. The customer probably wants try-on imagery for an event scoring this high. |

**Generate ≠ deploy.** "Auto-generate" here means the agent runs the score → curate → build chain locally and writes the lookbook to `~/.buck-mason-stylist/runs/<lookbook_id>/deploy/`. It does **not** mean the agent deploys the URL publicly — that step still requires `profile.md → preferred_lookbook_host_auto: true` per `references/headless-mode.md`. Without `_auto: true`, an auto-generated lookbook lands locally with a summary saying "ready to deploy"; the customer publishes interactively when ready.

Auto-generation runs in headless mode (`references/headless-mode.md`) — silent unless there's a result or blocker. The customer receives the run summary on their notification channel.

## Worked examples

| Event | type | dress | duration | location | signal | total | action |
|---|---|---|---|---|---|---|---|
| "Sarah & Tom's wedding · Sonoma · May 9–11 · smart casual" | 4 | 3 | 1 | 1 | 0 | 9 | Premium auto-generate |
| "Stripe Sessions · SF · Apr 26–28" | 2 | 0 | 1 | 1 | 0 | 4 | Skip (under 6) — but the customer's prior interaction asked for it, so customer_signal = +2 → 6 → soft surface |
| "Friday dinner — Bestia" | 2 | 2 | 0 | 0 | 0 | 4 | Skip silently |
| "Friday dinner — Bestia (smart casual)" | 2 | 3 | 0 | 0 | 0 | 5 | Skip silently |
| "Paris vacation · Jun 12–18" | 3 | 2 | 1 | 1 | 0 | 7 | Editorial auto-generate |
| "Annual physical with Dr. Lee" | -10 | 0 | 0 | 0 | 0 | -10 | Hard skip |
| "1:1 with Jamie" | 0 | 0 | 0 | 0 | 0 | 0 | Skip silently |
| "Block: focus time" | 0 | 0 | 0 | 0 | 0 | 0 | Skip silently |
| "Tycho · Greek Theater · Aug 14" | 2 | 2 | 0 | 0 | 0 | 4 | Skip silently — but a customer who's asked the agent to flag concerts before would push to 5–6 |

## Why this is conservative

The agent's value in calendar-driven mode is "I noticed something useful you might miss" — that requires very high precision. False positives ("you have a dentist appt coming up, want a lookbook?") destroy trust faster than false negatives ("the agent didn't flag the wedding"). The rubric weights are tuned so that ≥6 fires only on events where most customers would say "yes, that's a real wardrobe moment."

## How to implement

The scoring lives in `scripts/score-calendar-event.py`. Pass an event object (title, description, dress code, duration, location, customer-history snippets) on stdin or as JSON; get back `{ score, breakdown, action }`. The script is deterministic and side-effect-free — agents call it many times per calendar pass without billing or rate-limit concerns.

## Composition with other docs

- The triggered run uses `references/headless-mode.md` to actually generate the lookbook. The score determines *whether* to fire; headless mode determines *how*.
- The customer can disable calendar-driven scoring entirely by setting `profile.md → calendar_scoring: off`. Default is `on` once the customer has connected a calendar source — but **never auto-enabled without an explicit calendar connection**, which is itself an opt-in.
