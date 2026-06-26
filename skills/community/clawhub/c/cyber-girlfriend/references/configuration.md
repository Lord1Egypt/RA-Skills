# Configuration

Keep the runtime file name as `config.local.json` for compatibility.
Do **not** rename it for v2. Upgrade by adding `"version": 2` and the new sections.

## Design Goal

Ask the user for as little as possible.

Split the config into three kinds of fields:
1. **Companion character profile pointer** — where the Markdown character profile lives
2. **Owner identity boundary** — who the owner is, kept separate from companion life
3. **Agent-generated life model** — derived rhythm, current day schedule, continuity state

The user should mostly fill the first two kinds. The agent/runtime should generate the third kind.

## Field Ownership Rule

For first-time setup, keep this split strict:

- `config.local.json` stores profile paths, delivery, pacing policy, runtime paths, and optional long-lived source toggles
- `character-profile.md` stores the companion's core identity, tone, relationship expression, interests, and lived anchors
- `life_schedule.day_schedule.required_events` stores stable user-defined life anchors
- presence cron payloads store only the current runner chain, not long prompt prose
- generated state files store derived rhythm, continuity, and current day schedules

Do not turn `config.local.json` into a dump of prompt prose.

## Required Sections

### `version`

- Set to `2`

### `character_profile_path`

Path to the companion's core Markdown character profile.

Recommended:
- `./state/character-profile.md`

The published example is:
- `assets/character-profile.example.md`

This file now owns the full companion persona:
- name and owner-facing nickname
- age / life stage
- identity role
- city / district
- school, work, or creative background
- personality, interests, entertainment tastes, expression style, relationship style, and safety boundaries

### `persona` (deprecated)

Deprecated compatibility cache. New installs should not ask users to maintain this JSON object.

If an older `config.local.json` still has `persona`, it may be used as a migration source or fallback.
The forward direction is to migrate those fields into `character-profile.md` and keep config JSON focused on machine-readable runtime settings.

### `owner_profile`

Optional lightweight owner identity boundary. Its job is not to over-control style; its job is to stop the companion's school, work, friends, dorm, class, or other private-life material from being projected onto the owner.

Recommended fields:
- `source` — `manual | user_md | none`
- `user_md_path` — optional path when importing from OpenClaw `USER.md`
- `name`
- `preferred_name`
- `pronouns`
- `location`
- `timezone`
- `identity_summary`
- `not_assumptions` — optional user-defined taboos or identity assumptions to avoid

For first-time setup or upgrade, ask one product question:
`owner 信息要从 USER.md 导入，还是你手动自定义？`

If the user picks `USER.md`, import only stable identity fields such as name, preferred name, pronouns, location, and timezone. Do not copy messaging-platform session keys, account IDs, direct-chat IDs, or routing rules into prompt-facing outputs.

Do not add a `communication_style` field by default. The agent should infer communication from `character-profile.md`, relationship guardrails, and the owner boundary.

### `relationship`

Companion relationship guardrails.

Recommended fields:
- `mode`
- `intimacy_baseline`
- `jealousy_allowed`
- `clinginess_ceiling`
- `conflict_style`

### `delivery`

Outbound target configuration.

Required fields:
- `channel`
- `owner_target`

Optional:
- `account`
- `owner_session_key` as a deprecated compatibility value for older native heartbeat installs

First-time setup rule:
- ask for the real DM target id, not the current control UI label
- if the selected channel requires a sender account, capture it now instead of leaving it implicit

### `timezone`

Use the owner's real timezone / the companion's lived timezone.
This is required because the private-life layer should track real-world dates,
holidays, and time-of-day rhythms.

### `schedule`

Keep only pacing policy here.

Required fields:
- `quiet_hours_start`
- `quiet_hours_end`

Do **not** store her personal life schedule here.
Presence cron cadence belongs to OpenClaw cron configuration. Her lived day belongs to `day-schedule.md`.

Use this section only for:
- quiet hours

Do not try to encode fixed time-slot task text here.

旧安装里如果仍有 `cooldown_sec`，迁移后应删除。Heartbeat pacing is now
driven by the current `day-schedule.md` event plus pending-delivery and
same-event duplicate guards.

### `behavior`

Runtime behavior fields.

Recommended fields:
- `emotion_thresholds.present_sec`
- `emotion_thresholds.slightly_needy_sec`
- `emotion_thresholds.misses_him_sec`

Default values when the user has no preference:
- `present_sec`: `7200`
- `slightly_needy_sec`: `10800`
- `misses_him_sec`: `14400`

Optional but recommended:
- `derived_profile`
  - `activity_level`
  - `social_energy`
  - `sleep_profile`
  - `weekend_outdoor_bias`
  - `expression_density`

`derived_profile` should be generated by the agent from `character-profile.md`,
not manually filled by the user unless they want an override.

For new users, prefer generating `derived_profile` automatically after the character profile is captured. Do not block first setup on these knobs.

### `life_schedule`

This is the new private-life layer.
It should drive the companion's own lived context.

Recommended fields:
- `enabled`
- `day_schedule`
  - `enabled`
  - `schedule_path`
  - `refresh_mode`
  - `midday_refresh`
  - `required_events`
- `continuity`
  - `enabled`
  - `life_log_path`

`required_events` holds user-defined life anchors that should appear in the daily schedule as `必定发生：是`. These anchors are not render spec fields and do not guarantee that a message is sent.

Optional `media_hint` can be used when a required event should create media. The daily schedule builder should turn `media_hint` into the event's `媒体信息` field. For example, a 19:30 required event can ask to share one life photo whose concrete scene is derived from that day's main schedule rather than fixed in config.

### `runtime`

Externalize runtime hooks here.

Suggested fields:
- `workspace_root`
- `sessions_store_path`
- `state_file`
- `healthcheck_command`
- `cron_jobs_file`
- `jobs_list_command`

`sessions_store_path` is used for runtime state inspection and compatibility. Current `companion-presence` runs from an isolated cron session that calls `companion_presence_tick.py`; the wrapper starts the stable companion runtime session only after fresh prepare matches an event. Media events start OpenClaw async generation, and the wrapper also starts `companion_presence_tick.py --watch-recent-media-task` so generated media is sent through the explicit `delivery_contract` after the media task succeeds. Event state is committed after the text presence story is visibly sent, not after media success.

中文说明：异步媒体补发由 wrapper 后台 `--watch-recent-media-task` 自动等待任务完成并显式发送；原生 completion 不再是正确渠道投递的主路径，避免 runtime 把 current chat 误解为 Codex `internal-ui`。


### `sources`

Optional reality-sync sources.

Suggested blocks:
- `calendar_context`
- `weather_context`

## State Files

Recommended private-life files:
- `companion-state.json` — pacing + relationship state
- `day-schedule.md` — today's concrete event schedule
- `life-log.jsonl` — continuity claims already used in sent messages
- task-specific source files only when a concrete cron really needs them

## Upgrade Rule

For old installs:
- keep the same `config.local.json` path
- add `"version": 2`
- preserve existing `delivery` / `schedule` / `runtime`
- append `relationship`, `behavior.emotion_thresholds`, and `life_schedule`
- let the agent populate `behavior.derived_profile` automatically

For persona migration, use `migrate_config.py`. It reads the deprecated `persona`
block, writes `character-profile.md` when the profile does not already exist,
sets `character_profile_path`, and validates the generated profile:

```bash
python3 scripts/migrate_config.py --config config.local.json --write
```

Use `--overwrite-character-profile` only when the user explicitly wants to replace an existing profile.

Without `--write`, the command only prints the migration summary and does not create the profile. Character-profile validation runs after writing unless `--skip-character-profile-validation` is passed.

Use [standard-init-upgrade-flow.md](./standard-init-upgrade-flow.md) for the full upgrade checklist, including cron payload updates and real delivery verification.

## Validation Rule

The schema should validate a fully materialized v2 config, but the onboarding
agent may still bootstrap missing generated fields before first real use.

Before calling setup complete, the generated local config must be materialized:
- no placeholder strings such as `<REQUIRED_CHANNEL>` or `<RUNTIME_SPECIFIC>`
- all runtime paths point at the actual machine layout
- `runtime.state_file` parent exists or can be created
- `life_schedule` paths point at the intended state directory when enabled
- `delivery.owner_target` and sender account match the real outbound channel

## First-Time Setup Reminder

For a fresh install, pair this file with [first-time-setup.md](./first-time-setup.md):

- this file defines where fields belong
- `first-time-setup.md` defines what to ask, what to default, and what should stay in presence cron instead of config
