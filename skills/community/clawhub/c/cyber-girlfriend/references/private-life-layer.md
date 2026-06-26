# Private Life Layer

This reference defines the companion's own lived-context layer.

Use it when implementing or updating:
- daily schedule compilation
- required life event anchors
- continuity logging across proactive messages
- presence cron context injection

## Goal

Give the companion a believable private life without turning the system into heavy roleplay.

The companion should feel like:
- she already had a day before messaging the owner
- she has continuity across days
- she lives in the same real-world calendar/timezone as the owner
- she can lightly react to holidays, weather, and topical events
- her daily rhythm is constrained by who she is in the real world

The companion should not feel like:
- an improv soap opera
- a manipulative relationship sim
- a minute-by-minute scheduler
- a spammy diary bot
- a mirror that projects her school/work/private life onto the owner

## Three Layers

Keep owner identity as a separate config boundary. The private-life layer belongs to the companion; school, dorm, classmate, coursework, workplace, commute, and friend details must not be assumed to describe the owner unless the owner profile explicitly says so.

### 1. Character Profile Layer

This is who she is.

The file is `character-profile.md`, usually at `./state/character-profile.md`.

It owns:
- name and owner-facing nickname
- age / life stage
- identity role
- city / district when relevant
- institution, workplace, creative background, or focus area
- personality, interests, entertainment tastes, and relationship expression
- speech habits and safety boundaries

`config.local.json -> persona` is deprecated. Older JSON persona values may be used as migration input, but new installs should keep the companion's core character in Markdown.

### 2. Daily Schedule Layer

This is what is likely true today.

It should include:
- day type
- weather / season hints
- 3-5 ordinary `HH:mm - event title` schedule events outside configured quiet hours
- configured required events from `life_schedule.day_schedule.required_events`
- `必定发生：否` for ordinary events and `必定发生：是` for required events
- event scene, current activity, emotional state, mentionable detail, owner interaction entry, and avoid guidance
- continuity notes from recent interactions

Required events do not count toward the 3-5 ordinary event quota. They are life anchors, not guaranteed sends.

The daily schedule should not include quiet-hour policy itself. Quiet hours are read from local skill config.

### 3. Continuity Layer

Every successful proactive message may contribute a few `life_claims`.

Examples:
- "今天外面很闷"
- "刚从便利店回来"
- "晚上可能会慢慢收尾"

These claims should be appended to `life-log.jsonl` and used to prevent repetition and contradictions.

## Runtime Use Pattern

Recommended flow:

1. daily planning generates `day-schedule.md`
2. `companion-presence` runs in an isolated cron session and calls `companion_presence_tick.py`
3. the wrapper runs fresh prepare and selects the current real-time event from `day-schedule.md`
4. only matched events start the stable companion runtime session
5. the runtime writes one first-person companion message
6. the runtime calls `companion_presence_tick.py --send-story`; that fixed entrypoint sends through the explicit delivery contract and commits state after successful text delivery
7. media events then start OpenClaw async media generation, and native completion in the same stable companion session only provides fallback media paths

Presence cron does not manually assemble the life layer and does not pass `--event-time`.

## Realism Rules

- Prefer light slices of life over full status reports.
- Mention at most 1-2 life details per message by default.
- Do not make every message about the owner.
- Do not make every message about her own life either.
- Blend her life context with owner context naturally.
- Avoid high-drama events unless the user explicitly wants that mode.

## What Daily Schedule Should Produce

Good daily output:
- 3-5 concrete but low-drama ordinary events
- additional required events from config anchors when present
- `HH:mm` event headings outside configured quiet hours
- every event has `必定发生：是/否`, `执行时间`, and `媒体信息`
- a few mentionable details attached to real event scenes
- no duplicate event type in one day, including ordinary events duplicating required anchors

Bad daily output:
- fake certainty about exact actions
- a huge narrative paragraph
- a mechanical punch-clock timetable
- too many named side characters
- contradictions with yesterday's sent message

## Minimal Injection Contract

Presence cron calls `companion_presence_tick.py`; the wrapper calls `companion_run.py --stage prepare` so the runner selects the matching current event from `day-schedule.md`, then emits structured `life_context`.

Events marked `必定发生：是` are life anchors. If presence cron does not run inside that event window, the system does not backfill a forced message.

The final message should feel like:
- she already existed before this message
- she is sharing a small slice, not narrating a report
