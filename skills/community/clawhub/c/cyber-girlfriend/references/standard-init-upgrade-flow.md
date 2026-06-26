# Standard Init / Upgrade Flow

Use this reference for any OpenClaw setup that is more than a one-off wording tweak.

Apply it to:
- first-time setup
- full rebuild
- migration after a skill upgrade
- structural changes such as delivery rerouting, private-life enablement, or cron chain changes

Do not use the full rebuild flow for a small isolated request. In that case, keep the existing system and modify only the requested scope.

## Core Rules

1. `config.local.json` stores only stable configuration: character profile path, owner boundary, delivery, quiet hours, paths, and feature toggles.
2. `character-profile.md` and `day-schedule.md` own companion life text.
3. `life_schedule.day_schedule.required_events` defines required life anchors, not guaranteed sends.
4. `companion-build-day-schedule` must explicitly call web search before ordinary event generation and must consume those public materials inside normal character behavior events.
5. `companion-presence` is the only default user-facing proactive cron.
6. `companion-presence` runs in an isolated cron session and only calls the deterministic wrapper; the wrapper starts the stable companion session only after a matched event.
7. Media events are complete after the text presence story is visibly sent and committed; async media success is a follow-up enhancement, not the event completion gate.
8. Do not claim setup or upgrade is complete before a user-visible verification passes.

## Required Reading By Task

Always read:
- [../SKILL.md](../SKILL.md)
- [configuration.md](./configuration.md)
- [presence-integration.md](./presence-integration.md)
- [private-life-cron-templates.md](./private-life-cron-templates.md)
- [contract-schema.md](./contract-schema.md)

Read when doing first-time setup or rebuild:
- [first-time-setup.md](./first-time-setup.md)
- [agent-first-time-qa-template.md](./agent-first-time-qa-template.md)
- [required-events-and-cron.md](./required-events-and-cron.md)

Read when the scope needs them:
- [private-life-layer.md](./private-life-layer.md)
- [private-life-prompt-templates.md](./private-life-prompt-templates.md)
- [presence-integration.md](./presence-integration.md)
- [required-events-and-cron.md](./required-events-and-cron.md)

## First-Time Setup / Rebuild

### 1. Lock the delivery route first

Confirm:
- `delivery.channel`
- `delivery.owner_target`
- sender account if the channel requires it
- whether the current chat is only a configuration session or is also a delivery target

Do not create `companion-presence` until the outbound target is explicit.

### 2. Collect real-world persona anchors

First collect the owner identity boundary:
- ask whether to import owner info from OpenClaw `USER.md` or customize manually
- keep `owner_profile` lightweight
- never copy channel ids, account ids, DM targets, or session keys from `USER.md` into prompt-facing context

If the user wants the private-life layer or stronger "alive" feeling, capture enough real-world detail to support day-schedule generation:
- name / calling style
- age or life stage
- concrete role such as student, office worker, creator, artist
- city and, when known, a more local area
- school, workplace, or creative background when relevant
- interests and entertainment lanes
- hard boundaries

### 3. Capture required event anchors

Ask whether the user wants any things that should always be present in her day, for example a daily commute, evening gym time, a class, a photo walk, or a night wrap-up habit.

For each anchor, capture:
- title
- preferred time or time window
- duration
- scene
- activity
- natural mention
- owner interaction entry
- avoid rule

Store these in `life_schedule.day_schedule.required_events`. The daily builder writes them into `day-schedule.md` as `必定发生：是`.

### 4. Write and validate `config.local.json`

Write:
- `character_profile_path`
- `owner_profile`
- `relationship`
- `delivery`
- `timezone`
- quiet hours
- runtime/state paths
- `life_schedule` enablement, file paths, and required event anchors

Rules:
- valid JSON
- fully materialized: no `<REQUIRED_...>`, `<RUNTIME_SPECIFIC>`, or copied example values remain
- no secrets in prompt-facing files
- no full cron prompt prose in config

### 5. Generate current day context immediately

When private life is enabled:

1. create or refresh `character-profile.md`
2. create or refresh `day-schedule.md`
3. validate both files

`day-schedule.md` must have 3-5 ordinary events marked `必定发生：否`. Required event anchors are additional `必定发生：是` events and do not count toward that quota. Before ordinary events are generated, the builder must search 4-5 public, non-sensitive keywords extracted from the character profile: one city/weather keyword, one local area/school/workplace/community keyword, one identity/occupation keyword, and one or two interest keywords. Each searched category must be consumed by at least one event through the event scene, action, natural mention, or avoid rule. Every event also keeps a `媒体信息` field; leave it empty unless the event should produce a photo, audio, video, or similar media artifact. Ordinary events must not duplicate each other or duplicate configured required events by type/content.

### 6. Create or update cron jobs

Recommended creation order:

1. `companion-build-day-schedule`
2. `companion-presence`

`companion-presence` contract:

1. cron 运行在 isolated session 中
2. 第一个也是唯一业务动作是触发 `companion_presence_tick.py --config <CONFIG>`
3. 脚本输出任何已处理状态后只回复 `NO_REPLY`
4. cron payload 不直接读取 `day-schedule.md`，不直接判断事件，也不自己处理消息发送或媒体生成
5. wrapper 内部 fresh prepare；只有命中事件时才启动稳定 companion session
6. 稳定 companion session 负责写文本、按 `delivery_contract` 投递；文本可见投递成功后立即提交状态，媒体事件随后启动异步媒体，wrapper 后台 `--watch-recent-media-task` 负责补发媒体

Do not pass `--event-time`. Presence cron reads the current real local time.

### 7. Run a real verification

Check:
- the user can actually see the message
- no duplicate delivery occurred
- `skip` behavior still works when no current event is active
- state advances only after confirmed delivery
- media failure or completion timeout does not block the event after the text was delivered and committed
- life log updates when continuity logging is enabled
- the user-facing message does not expose scripts, cron, JSON, tools, or system internals

If verification fails, fix routing and task flow first.

## Upgrade / Migration Flow

### 1. Snapshot the current install

Before changing structure, preserve:
- current `config.local.json`
- state files
- cron list and payloads
- any documented custom user tasks or fixed daily habits

### 2. Audit the new skill shape

List what changed:
- config fields added or deprecated
- cron chain changes
- new or removed scripts
- delivery rule changes
- private-life model changes
- legacy render-chain removal

### 3. Preserve user intent

Do not lose:
- character/persona
- hard boundaries
- delivery target
- quiet hours
- custom fixed daily habits
- continuity state

Old `morning` / `afternoon` / `evening` / `night` content cron tasks should be converted to required event anchors when they represent "something she should be doing". If they represent a real external task, preserve the task intent in a clearly documented custom integration outside `companion_run.py`.

### 4. Migrate each concern to the correct layer

Keep ownership clean:
- stable settings -> config
- core character -> `character-profile.md`
- dynamic day context -> state Markdown files
- fixed life anchors -> `life_schedule.day_schedule.required_events`
- delivery behavior -> `companion-presence`

### 5. Fill in new required layers

Config field migration checklist:
- `version`: set to `2`
- `character_profile_path`: point at `./state/character-profile.md` or the real local profile path
- `owner_profile`: add a lightweight owner boundary
- `delivery`: preserve `channel`, `owner_target`, and sender account
- `schedule`: preserve quiet hours; do not move cron times into config
- `relationship`: add defaults if missing
- `behavior.emotion_thresholds`: add defaults if missing
- `life_schedule`: add day-schedule/continuity paths and required event anchors when private-life is enabled
- `runtime`: preserve real local paths
- placeholders: remove every copied example value before verification

Prefer the helper:

```bash
python3 scripts/migrate_config.py --config <CONFIG> --owner-source user_md --write
```

If the install has old `persona`, `month-plan.json`, or `day-context.json`, migrate only the stable character facts and today's usable day context; do not recreate a weekly plan layer.

### 6. Upgrade cron payloads carefully

For current architecture:

1. disable deprecated visible content cron jobs unless the user explicitly keeps them as custom jobs
2. create or update `companion-build-day-schedule`
3. create or update `companion-presence` as an isolated cron session that calls `companion_presence_tick.py`
4. ensure the wrapper uses prepare with `--no-record-pending` and starts the stable companion session only on `status = "ok"`
5. ensure `companion-build-day-schedule` explicitly requires web search and category-level search consumption before writing `day-schedule.md`
6. ensure the final message is delivered through `companion_presence_tick.py --send-story`, which uses the saved delivery contract and commits state only after send succeeds
7. ensure media events start async media only after `--send-story` succeeds, then use the wrapper-launched `--watch-recent-media-task` so generated media is sent with the saved delivery contract; native media completion is only a fallback and must not rely on current chat

Remove old references to:
- `--event-time`
- render spec `required_events`
- render spec `schedule_event`
- `--stage render`
- `final_message_contract`
- native heartbeat transcript reconciliation
- old multi-script life prompt/render helpers

### 7. Completion Checklist

Do not declare success without checking:
- config valid
- `python3 scripts/validate_release.py --root <SKILL_DIR> --config <CONFIG>` passes for publishable skill changes
- `character-profile.md` valid
- `day-schedule.md` valid when enabled
- required planner jobs exist when enabled
- `companion-presence` follows the current runner contract
- prepare output has `life_context`, `delivery_contract`, and `state_commit`, not `render_spec` or top-level `primary_goal`
- media contracts do not expose local runbook paths
- native media completion can return to the stable companion session, but correct-channel media delivery is handled by the wrapper watcher after the presence turn has ended
- at least one visible delivery test passed
- user customization was preserved

## Common Failure Modes

Avoid these:
- reading only `SKILL.md` and skipping the references needed for the actual task
- creating `companion-presence` before the delivery route is explicit
- leaving old four-slot content cron jobs enabled after migrating to presence cron
- dumping dynamic day content into config
- asking the user to write prompts
- treating "one message was sent" as proof that setup is complete
- advancing sent/progress state after a failed or unverified delivery
- leaking scripts, cron, JSON, or tool details into owner-facing messages
