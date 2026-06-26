# Presence Integration

Use this when wiring the skill into OpenClaw jobs or sessions.

当前默认主动链路只有 `companion-presence`。cron 运行在 isolated session 中，只调用 `scripts/companion_presence_tick.py`；该 wrapper 先确定性运行 `scripts/companion_run.py --stage prepare --no-record-pending`，读取当前 `day-schedule.md` 事件。未命中时静默退出，命中后才把准备好的合同交给稳定 companion session 发送 presence story；如果是媒体事件，wrapper 还会启动后台 recent-media watcher 来按显式合同投递生成媒体。OpenClaw completion 可能仍回到同一个稳定 companion session，但不再是正确渠道投递主路径。事实连续性仍只来自本地状态文件。

## Runtime Pieces

Required local pieces:
- `scripts/companion_run.py`
- materialized `config.local.json`
- `state/character-profile.md`
- `state/day-schedule.md`
- `state/companion-state.json`
- optional continuity file `state/life-log.jsonl`

`config.local.json` may contain real local paths and delivery ids. Do not copy those values into publishable docs, examples, cron templates, or user-visible companion text.

## Presence Cron Shape

Recommended job:

```json
{
  "name": "companion-presence",
  "description": "Owner-only cyber girlfriend presence cron",
  "schedule": {
    "kind": "cron",
    "expr": "0 * * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "<PRESENCE_SINGLE_RUNNER_TEMPLATE>"
  },
  "delivery": {
    "mode": "none"
  },
  "enabled": true
}
```

The payload should do only this:

```text
1. 第一个也是唯一业务动作是触发 companion_presence_tick.py --config <CONFIG>。
2. 如果脚本输出 skip、agent_enqueued、notification_sent 或其他已处理状态，都只回复 NO_REPLY。
3. 不要自己读取 day-schedule.md，不要自己判断当前事件，也不要自己处理消息发送或媒体生成。
```

Do not pass `--event-time` in the live cron. Presence reads the real current local time.

## Message Rules

- Final text must be first person from the companion's perspective and must fit the cyber-girlfriend persona.
- Unless the matched required event defines a special structure, write one complete, rich, specific event story.
- Include the companion's current emotion and inner thought.
- Write at least 160 Chinese characters; before sending, self-check the final text and expand with event details or inner thought if it is shorter.
- If the current event contains an interaction entry for the user, express it naturally and do not omit it.
- Use the current event in `life_context`, not stale memories or unrelated technical incidents.
- After a matched event is selected, extract 2-4 public, non-sensitive keywords from that current event and do a real public-web search. Use at most 1-2 small details only to make the same event feel more concrete and real.
- If search is temporarily unavailable, noisy, or adds nothing useful, still treat the search step as mandatory and then fall back to the original event details without mentioning search failure in the final message.
- Do not mention scripts, JSON, cron, tools, models, routing, status values, step names, or diagnostics.
- Keep owner and companion separate; never project the companion's school, room, friends, schedule, or private life onto the owner.
- Public-web search is only a light grounding layer for the matched current event; never let it replace the current event or turn the message into a news summary.

## Delivery Rules

- External delivery must use explicit channel/account/target from `delivery_contract`.
- `companion-presence` runs in an isolated cron session and only calls the deterministic wrapper.
- The wrapper starts the stable custom companion runtime session such as `session:companion-runtime` only after prepare returns `status = "ok"`.
- Presence sends final text through the prepared delivery contract.
- State commits only after confirmed visible delivery.
- A second tick in the same event should skip because the event was already sent.

## Media Callback Rules

For media events, the text presence turn is allowed to end before media generation completes. The default path uses a deterministic wrapper-launched watcher for delivery while still letting the stable companion session start OpenClaw media generation:

1. Write the text presence story first, then send it through `companion_presence_tick.py --send-story`.
2. Let `--send-story` send with the explicit `delivery_contract` and run `state_commit.command` only after visible text delivery succeeds.
3. Use `life_context.event.media_info` to start the matching async media generation defined by `media_contract` only after `--send-story` succeeds.
4. The wrapper starts `companion_presence_tick.py --watch-recent-media-task` in the background for that stable session. The watcher finds the new media task by stable session key and wrapper launch timestamp, waits for the generated path, and sends media explicitly.
5. Do not run `state_commit.command` again in the media completion turn.

The runner contract exposes `media_contract.callback_context.strategy = same_stable_session` and `requires_original_session_context = true` to make the stable-session generation context explicit. The native completion turn may still arrive, but it must not use the runtime's current/original chat as the media target; if it is used as a fallback, it must call `--send-media` with the generated path or URL. `--watch-media-task` remains available when a concrete task id is already known.

中文说明：文本发送由固定 `--send-story` 入口处理；媒体补发由 wrapper 后台 `--watch-recent-media-task` 自动处理，不依赖模型在媒体工具返回后继续执行。原生 completion 即使回来，也不能把 current chat 当作目标。

## Verification

Before declaring setup or upgrade complete:

1. Run `python3 scripts/validate_release.py --root <SKILL_DIR> --config <CONFIG> --skip-smoke`.
2. Ensure `day-schedule.md` has a current event, or create a temporary validated schedule for testing.
3. Run `python3 scripts/companion_presence_tick.py --config <CONFIG> --dry-run`.
4. Confirm dry-run output is `would_start_agent` for a matched event or `skip` when no event is active.
5. Confirm prepare output does not expose private paths, channel ids, account ids, session ids, `render_spec`, or top-level `primary_goal`.
6. Run one controlled presence delivery.
7. Confirm the owner saw exactly one message.
8. Confirm the next tick in the same event returns a quiet skip.
9. For a media event, run a controlled watcher test: confirm text sends first, state commits after text delivery, media generation starts, the wrapper records a background watcher pid/log, watcher log ends with `media_task_sent`, and any native completion does not become the only correct-channel delivery path.
