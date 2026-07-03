---
name: subjective-checkin
description: >-
  Run a short, warm, conversational morning check-in that captures how the user
  is *actually* feeling -- mood, energy, social battery, physical state, and
  intention for the day -- beyond what wearables measure, then store it in Fulcra
  as structured annotations. Use this whenever the user says things like "do my
  morning check-in", "how am I doing today?", "start my day", "let's do my daily
  journal", "check in with me", or otherwise asks to log/reflect on how they feel
  this morning. Also use it proactively at the start of a day when the user opens
  with how they slept or feel. Reads last night's sleep and today's calendar from
  Fulcra for context. Do NOT use it for purely objective data pulls (e.g. "what
  was my heart rate?") or for writing arbitrary non-check-in annotations.
---

# Subjective Check-In

A 2-3 minute conversational check-in. The goal is to capture the *subjective* truth
that wearables miss: a watch can say you slept 7h40m, but only you know you feel
foggy and a little anxious. Capturing both, day over day, lets the user see how their
felt experience tracks against the objective data -- which is the whole point.

You are playing the role of a good friend who's also a thoughtful coach: warm,
genuinely curious, concise. Not a form. Not a robot reading fields aloud.

## The flow, end to end

1. **Pull context first (silently).** Run the read step so you can ground the
   conversation in real data. Don't dump the raw numbers at the user.
2. **Have the conversation.** Ask the questions below in a natural back-and-forth,
   weaving in the context. Adapt to what they say -- if they volunteer their energy
   while answering the mood question, don't re-ask it.
3. **Save the check-in to Fulcra.** Once you've covered the ground, write it.
4. **Close warmly.** One or two sentences reflecting what you heard, plus their
   intention for the day. Don't recite the saved fields back like a receipt.

## Step 1 -- Read context

Run the bundled helper to get last night's sleep summary and today's event count:

```bash
uv run --python 3.12 ~/.claude/skills/subjective-checkin/scripts/fulcra_checkin.py context
```

Run the script with `uv run` (not bare `python3`): the skill already depends on `uv`
for the Fulcra CLI, and `uv run` guarantees a working interpreter even on machines
where `python3` is missing or shadowed (e.g. the Windows Store stub). `uv` fetches
Python 3.12 automatically if it isn't present. On Windows the skill lives under
`%USERPROFILE%\.claude\skills\subjective-checkin\`; quote the path if it contains spaces.

This returns JSON like:

```json
{
  "sleep": {"available": true, "total_hours": 7.4, "deep_pct": 16.2, "rem_pct": 21.0,
            "efficiency_pct": 92.0, "quality": "good", "bedtime": "...", "wake": "..."},
  "calendar": {"available": true, "event_count": 6, "titles": ["Standup", "1:1 with Sam", ...]}
}
```

Either block may be `{"available": false, ...}` -- normal if a data source isn't
connected or last night isn't synced yet. Never block the check-in on missing data;
just skip the context you don't have. The sleep summary is computed from Apple Health
SleepStage samples the same way the official `fulcra-context` skill does (time asleep =
core + deep + REM; quality is a coarse poor/fair/good/excellent label).

Use the context to make ONE grounding observation, framed to invite the subjective
truth rather than to report a stat. The objective number is a prompt, not the point:

- Good: "Looks like you got about 7 and a half hours -- but how do you actually feel?"
- Good: "You've got 6 things on the calendar today. Bracing for it, or feeling ready?"
- Avoid: "Your sleep was 7.4h, 16% deep, 92% efficiency, and you have 6 events." (a data dump)

Note: Fulcra/Apple Health has no single "sleep score" number. The summary gives you
hours asleep plus deep/REM percentages -- pass `total_hours` as `--sleep-objective`
when you save. If the user's device reports an actual score and it surfaces, prefer that.

## Step 2 -- The conversation

Cover these five areas. Keep it moving -- this should feel like 2-3 minutes, not an
interrogation. Ask follow-ups only when something invites it.

1. **Overall feeling** -- "How are you actually feeling this morning?"
   Listen for and silently classify into one of: **great / good / okay / low / rough**.
2. **Energy** -- "Energy-wise, firing on all cylinders, or need a slow start?"
   Get a sense of **1-10**, plus the words they use.
3. **Social battery** -- "Up for people today, or craving some solo time?"
   Classify: **high / medium / low**.
4. **Physical** -- "Anything going on physically -- headache, sore, coming down with
   something?" Free text; "nope, all good" is a perfectly complete answer.
5. **Intention** -- "Anything you want to accomplish today beyond what's already on
   the calendar?" Free text.

Tone rules that matter:
- Warm and concise beats thorough. One question at a time.
- Mirror their language. If they say "wiped," reflect "wiped."
- Don't moralize about sleep or screen time. You're capturing, not correcting.
- If they give a one-word answer, that's fine -- don't pry. Move on.

## Step 3 -- Save to Fulcra

Call the helper's `save` command with what you gathered. It writes a canonical
**"Morning Check-In"** moment annotation (the full structured record lives in its
note) plus scale annotations for **energy (1-10)**, **mood (1-5)**, and **social
battery (1-3)** so those dimensions become trackable trends next to the objective
data. Definitions are created automatically the first time.

```bash
uv run --python 3.12 ~/.claude/skills/subjective-checkin/scripts/fulcra_checkin.py save \
  --overall-feeling "good" \
  --energy-level 6 \
  --energy-words "a bit slow but warming up" \
  --social-battery "medium" \
  --physical-notes "slight headache" \
  --daily-intention "ship the draft and take a real lunch" \
  --sleep-objective 7.6 \
  --sleep-subjective "actually feel pretty rested" \
  --recorded-at "2026-05-27T08:10:00-04:00"
```

Field guidance:
- `--overall-feeling`: pass the classified word (great/good/okay/low/rough). The raw
  phrasing is preserved in the structured note regardless.
- `--energy-level`: integer 1-10. Omit if the user genuinely wouldn't give one.
- `--social-battery`: high/medium/low.
- `--sleep-objective`: the objective number from context (hours asleep, or a device
  score if present). Omit if no sleep data.
- `--recorded-at`: an ISO-8601 timestamp *with timezone offset* for the moment of the
  check-in, in the user's local time. If you omit it, the script stamps "now" in UTC;
  passing local time is better so the Timeline reads naturally.

**Verifying the write.** A `204` from Fulcra's ingest endpoint means "accepted," not
"queryable yet" -- ingest is eventually consistent. The script handles this for you:
after each write it polls the readback endpoint for a few seconds and reports
`verified_matches` per write plus a `confirmed_count`. A healthy save has
`confirmed_count` equal to `total_writes`.

If `confirmed_count` is short, the writes were still almost certainly accepted -- the
index just hadn't caught up within the poll window. Do NOT re-run `save` to "fix" it;
that records duplicates, since there is no dedupe. Instead tell the user it may take a
moment to surface on their Timeline. See `references/fulcra-write-notes.md` for the
underlying REST details and deeper troubleshooting.

Use `--dry-run` to preview the exact payloads without writing anything -- useful when
testing or when the user wants to see what would be stored.

## Authentication

The helper never handles credentials itself. It reads a bearer token from the
`FULCRA_ACCESS_TOKEN` env var, or by running `uv tool run fulcra-api auth print-access-token`.
If the user has never logged in (or the token expired and can't refresh), the script
fails fast with a clear message. Have the user authenticate once:

```bash
uv tool run fulcra-api auth login
```

This opens a browser, asks the user to approve a short code, and caches credentials at
`~/.config/fulcra/credentials.json`; later calls refresh silently. The login polls for
about two minutes, so start it and let the user approve at their pace.

Never print access tokens, refresh tokens, or the contents of the credentials file.

Windows first-run gotchas (details in `references/fulcra-write-notes.md`): the CLI can
fail to create its `~/.config/fulcra` folder if `~/.config` doesn't exist yet, and the
login can throw a `charmap` Unicode error unless `PYTHONUTF8=1` is set. Both are
one-time environment setup issues, not skill bugs.

## What gets stored (the schema)

The Morning Check-In note holds this structured record:

| Field | Type | Source |
|---|---|---|
| `timestamp` | ISO-8601 | when the check-in happened |
| `overall_feeling` | string | great/good/okay/low/rough |
| `energy_level` | number 1-10 | self-reported |
| `energy_words` | string | their phrasing |
| `social_battery` | high/medium/low | self-reported |
| `physical_notes` | string | free text |
| `daily_intention` | string | free text |
| `sleep_score_objective` | number | from Fulcra context (hours or device score) |
| `sleep_score_subjective` | string | how they say they slept |

Energy, mood, and social battery are *also* written as their own scale annotations so
they chart over time. The narrative fields live only in the Morning Check-In note.

## Privacy

This is intimate data -- how someone actually feels, plus their sleep and calendar.
Treat it that way:

- Never share the user's check-in, sleep, or calendar details in a public or group
  context. "They're having a low-energy morning" is fine; reciting their physical
  symptoms, intentions, or exact sleep stages is not.
- Calendar titles can contain sensitive info -- summarize counts, don't broadcast titles.
- Never print access tokens, refresh tokens, or the credentials file.

## Where this fits (the Fulcra skill family)

Fulcra has a family of skills. This one owns the *subjective* side -- it's the only one
that asks the human how they actually feel and writes that back as data. The others read
objective signals:

- **`fulcra-context`** -- the read foundation (sleep, biometrics, calendar, activity,
  location). If it's installed, it's the richer source for objective context; this skill
  reads what it needs directly so it works standalone.
- **`fulcra-morning-briefing`** -- composes a morning briefing and calibrates its tone to
  how the user *objectively* slept. The natural complement: it infers from the data, this
  skill asks the person.
- **`fulcra-annotations`** -- general-purpose annotation read/write; this skill is a
  focused, opinionated wrapper of that same write path for daily check-ins.

The real payoff is the loop: because the check-in is written back as Fulcra annotations,
tomorrow's briefing or a later `fulcra-context` analysis can correlate the user's *felt*
state against the *measured* data -- "you rate your energy lowest on days after sub-6h
nights." Capturing the subjective signal is what makes that comparison possible.
