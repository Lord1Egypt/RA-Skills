# First-Time Setup Guide

Use this when a user is configuring the skill for the first time or rebuilding it from scratch.

Goal:
- collect only the minimum decisions the user must make
- keep delivery fields correct
- generate `character-profile.md` and `day-schedule.md`
- wire `companion-presence` without turning onboarding into prompt-writing
- treat user-defined fixed content as life anchors, not guaranteed sends

If you need literal onboarding wording, use [agent-first-time-qa-template.md](./agent-first-time-qa-template.md).

## First-Time Setup Order

Follow this order. Do not skip ahead to polishing wording.

1. Confirm the proactive delivery destination.
2. Decide whether owner info should be imported from `USER.md`, customized manually, or skipped.
3. Capture and write the companion's `character-profile.md`.
4. Ask whether the user wants any `必定发生：是` life anchors.
5. Write and materialize `config.local.json`.
6. Generate the first `day-schedule.md` with 3-5 ordinary events plus configured required events.
7. Create or update `companion-build-day-schedule` and `companion-presence`.
8. Run validation and one controlled user-visible verification.

## What The User Must Decide

Ask for or infer only these fields first:

| Question | Destination | Required? | Notes |
| --- | --- | --- | --- |
| Which channel should proactive messages use? | `delivery.channel` | yes | Example: direct message or another configured OpenClaw channel |
| What exact recipient id should delivery use? | `delivery.owner_target` | yes | Use the real target id, not the current UI label |
| Which sending account should be used? | `delivery.account` | channel-dependent | Required on channels that need a specific sender account |
| Import owner info from `USER.md` or customize manually? | `owner_profile` | recommended | Import only stable identity fields; never prompt with private channel/account ids |
| How old or what life stage is she? | `character-profile.md` | strongly recommended | Example: freshman, early-career, creator |
| What exactly is her real-world role? | `character-profile.md` | strongly recommended | Example: design intern, game content creator |
| Which city or district does she live around? | `character-profile.md` | strongly recommended | City alone is often too coarse for believable planning |
| What interests and entertainment does she naturally follow? | `character-profile.md` | strongly recommended | Used for daily reality anchors and local life texture |
| Any fixed things that should always enter her day? | `life_schedule.day_schedule.required_events` | optional | These become `必定发生：是` events, not guaranteed messages |
| Quiet hours? | `schedule.quiet_hours_start` / `schedule.quiet_hours_end` | yes | Default is fine when the user has no preference |

Do not ask for advanced style tuning, derived profile fields, low-level life-schedule internals, or legacy visible cron modes during the first pass.

## Owner Profile Rule

Keep owner information light. The setup only needs enough to distinguish owner from companion:
- `source`: `user_md`, `manual`, or `none`
- `preferred_name`
- `pronouns`
- `location`
- `timezone`
- optional `identity_summary`
- optional `not_assumptions`

When `USER.md` exists, offer import as the recommended path. Import only stable identity fields and do not copy routing identifiers, direct-chat IDs, account IDs, or session keys into prompt-facing context.

## Character Profile Detail Rule

If `life_schedule.enabled` is true or the user explicitly wants stronger 活人感, do not stop at a thin persona like "college student in a city".

At minimum, capture:
- life stage or age band
- concrete school, work, creator, or daily identity
- city plus a more local area when known
- interests plus the kinds of entertainment and content she actually follows

Write these into `character-profile.md`, not into `config.local.json -> persona`.

## Required Event Anchors

Required events are life facts. They make the daily schedule include something the user cares about, but they do not force a message to be sent.

For each anchor, capture:
- time window or preferred time
- title
- duration
- scene
- what she is doing
- what can be naturally mentioned
- owner interaction entry
- what not to write it as

Store anchors in `life_schedule.day_schedule.required_events`. The daily builder turns them into `day-schedule.md` events with `必定发生：是`.

## Recommended Starter Defaults

Use these when the user says "先给我一套能跑的" or has no strong preference:

- daily schedule builder: `10 7 * * *`, isolated, no delivery
- presence cron: hourly, isolated cron session that calls `companion_presence_tick.py`; the wrapper starts the stable companion runtime session only after a matched event
- quiet hours: `01:00` to `08:00`
- required events: none unless the user names one

The old four-slot content cron setup is deprecated. If the user asks for a fixed daily habit, model it as a required event anchor first.

## Materialized Config Gate

After writing `config.local.json`, verify it is not just a copied example.

Required before cron creation:
- no placeholder values like `<REQUIRED_CHANNEL>` or `<RUNTIME_SPECIFIC>`
- actual `character_profile_path`
- actual `runtime.workspace_root`
- actual `runtime.sessions_store_path`
- actual `runtime.state_file`
- actual `runtime.healthcheck_command`
- actual `life_schedule` state paths when enabled
- default `behavior.emotion_thresholds` if the user did not customize them

For rebuilds or scripted setup, use the migration helper to materialize defaults:

```bash
python3 scripts/migrate_config.py --config <CONFIG> --owner-source user_md --write
```

Use `--owner-source manual` or `--owner-source none` when the user chooses those paths.

## Markdown Life Text Initialization

When private life is enabled, initialize the Markdown files before creating presence cron. Do not leave the first real run to invent life context from an empty state directory.

Create or refresh these files in order:

1. `character-profile.md`
2. `day-schedule.md`

For `day-schedule.md`, derive today's 3-5 concrete ordinary events directly from the character profile, today's date, public search materials, recent life log, and configured required events. Before ordinary events are written, explicitly run web search with the standard 4-5 keyword mix: one city/weather keyword, one local area/school/workplace/community keyword, one identity/occupation keyword, and one or two interest keywords. Add required events into the same `## 4. 日程事件` section as `必定发生：是`.

Each event must have:
- `HH:mm - 事件标题`
- `必定发生：是/否`
- `执行时间`
- scene, action, mood, natural mention, interaction entry, media info, and avoid rule
- no quiet-hour overlap
- no overlapping event windows
- no duplicate event types in the same day, including duplicates with configured required events
- every searched category is consumed by at least one normal character behavior event rather than becoming a standalone news/material-browsing event

Run the Markdown validators immediately:

```bash
python3 scripts/validate_character_profile.py --profile <CHARACTER_PROFILE>
python3 scripts/validate_day_schedule.py --config <CONFIG> --path <DAY_SCHEDULE>
```

If validation fails, fix the Markdown file itself before creating cron jobs.

## Delivery Pitfalls To Prevent

Before creating cron jobs, make sure the onboarding agent has stated these rules:

- proactive outbound delivery follows the local config delivery block
- `companion-presence` runs in an isolated cron session, not the owner conversation
- `companion_presence_tick.py` starts the stable companion runtime session only after fresh prepare returns a matched event
- final companion text is sent through the prepared delivery contract
- state is committed only after visible text delivery succeeds
- media turns commit state after visible text delivery, then start OpenClaw async media generation; the native completion returns to the same stable companion session and only sends media
- required events are not guaranteed sends

## First Verification Gate

For a fresh install, do one controlled real run after setup:

1. Run `python3 scripts/validate_release.py --root <SKILL_DIR> --config <CONFIG> --skip-smoke`.
2. Ensure `day-schedule.md` has a current event or create a temporary validated test schedule.
3. Run `companion_run.py --stage prepare --config <CONFIG> --no-record-pending`.
4. Confirm the prepare contract has `life_context`, `delivery_contract`, `media_contract`, and `state_commit`; it must not have `render_spec`, `media_task_record_contract`, or top-level `primary_goal`.
5. Send one first-person companion presence story to the intended owner target through `companion_presence_tick.py --send-story`.
6. Confirm `--send-story` commits state only after text delivery succeeds. For media events, start async media after the commit; do not wait for media success to mark the event complete.

If delivery fails, fix routing first. Do not keep polishing personality copy while the send path is still untrusted.
