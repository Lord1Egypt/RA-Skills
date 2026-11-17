# Presence Integration

Use this when wiring the skill into OpenClaw jobs or sessions.

当前默认主动链路只有 `companion-presence`。支持 command automation 的 OpenClaw 运行时使用 exact argv payload 直接调用 `scripts/companion_presence_tick.py`，不先启动只负责执行 wrapper 的模型 turn；该 wrapper 再确定性运行 `scripts/companion_run.py --stage prepare --no-record-pending`，读取当前 `day-schedule.md` 事件。未命中时静默退出，命中后才按 run id 派生新的 dispatch session 并发送 presence story；如果是媒体事件，wrapper 还会启动后台 recent-media watcher 来按显式合同投递生成媒体。OpenClaw completion 可能仍回到同一个 dispatch session，但不再是正确渠道投递主路径。事实连续性仍只来自本地状态文件，不复用可能已归档的旧 session。

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
    "kind": "command",
    "argv": [
      "python3",
      "<SKILL_DIR>/scripts/companion_presence_tick.py",
      "--config",
      "<CONFIG_PATH>"
    ],
    "cwd": "<SKILL_DIR>",
    "env": {
      "PYTHONUNBUFFERED": "1"
    },
    "timeoutSeconds": 120,
    "outputMaxBytes": 65536
  },
  "delivery": {
    "mode": "none"
  },
  "enabled": true
}
```

Use exact argv rather than a shell string. The command payload is an operator-authored Gateway execution surface, so every executable and argument must be fixed by the installer; do not interpolate owner text, event text, config fields, or model output into the command.

CLI shape:

```bash
openclaw cron edit <JOB_ID> \
  --command-argv '["python3","<SKILL_DIR>/scripts/companion_presence_tick.py","--config","<CONFIG_PATH>"]' \
  --command-cwd '<SKILL_DIR>' \
  --command-env 'PYTHONUNBUFFERED=1' \
  --timeout-seconds 120 \
  --output-max-bytes 65536 \
  --session isolated \
  --no-deliver
```

OpenClaw 2026.8.1 的 `cron edit` 在 agent payload 转 command payload 时，省略 `--command-env` 可能把空 env 送入校验并报 `command env must be an object`。固定的 `PYTHONUNBUFFERED=1` 既规避该转换问题，也让 wrapper 输出及时进入任务日志；不要用该参数注入动态内容或秘密。

Older OpenClaw versions without command payloads may keep the legacy isolated `agentTurn` fallback. That compatibility payload must enable lightweight context, run only `companion_presence_tick.py --config <CONFIG>`, and reply `NO_REPLY` for every handled wrapper status. It is not the default for new or upgraded installations.

Do not pass `--event-time` in the live cron. Presence reads the real current local time.

## Authorization And Lifecycle Controls

Before creating, editing, or enabling either recurring job, read the current job definitions and preview the exact job ids/names, schedules, payload types, fixed argv, masked route, public-search use, and controlled verification send. Wait for explicit user confirmation before applying the preview or sending the test message.

Pause is reversible and must not delete local files:

```bash
openclaw cron disable <PRESENCE_JOB_ID>
openclaw cron disable <BUILDER_JOB_ID>
```

Resume only the exact jobs the user wants:

```bash
openclaw cron enable <BUILDER_JOB_ID>
openclaw cron enable <PRESENCE_JOB_ID>
```

Keep the previous job definitions until the edited jobs have passed validation so their payloads can be restored if needed. Use `openclaw cron rm <JOB_ID>` only after the user separately and explicitly requests permanent removal and the exact ids have been resolved. Pausing or rolling back jobs must not delete `config.local.json`, character/day Markdown, state, or continuity logs.

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
- `companion-presence` runs as an isolated exact argv command automation and only calls the deterministic wrapper.
- The wrapper derives a fresh companion session from the configured base key and prepared run id only after prepare returns `status = "ok"`.
- Presence sends final text through the prepared delivery contract.
- If the external CLI returns `prepare failed` or `Unknown channel` for `openclaw-weixin`, the same fixed send entrypoint may use the existing direct WeChat API fallback with that explicit contract; no model-selected route is allowed.
- State commits only after confirmed visible delivery.
- A failed fixed-entrypoint send records `delivery_failed`, which is retryable on the next tick instead of holding the event in `agent_started` until TTL expiry.
- A second tick in the same event should skip because the event was already sent.

## Media Callback Rules

For media events, the text presence turn is allowed to end before media generation completes. The default path uses a deterministic wrapper-launched watcher for delivery while still letting the dispatch-scoped companion session start OpenClaw media generation:

1. Write the text presence story first, then send it through `companion_presence_tick.py --send-story`.
2. Let `--send-story` send with the explicit `delivery_contract` and run `state_commit.command` only after visible text delivery succeeds.
3. Use `life_context.event.media_info` to start the matching async media generation defined by `media_contract` only after `--send-story` succeeds.
4. The wrapper starts `companion_presence_tick.py --watch-recent-media-task` in the background for that dispatch session. The watcher finds the new media task by dispatch session key and wrapper launch timestamp, waits for the generated path, and sends media explicitly.
5. Do not run `state_commit.command` again in the media completion turn.

The runner contract exposes `media_contract.callback_context.strategy = same_stable_session` and `requires_original_session_context = true`; here "stable" means the same session for this one dispatch and media lifecycle, not cross-event reuse. The native completion turn may still arrive, but it must not use the runtime's current/original chat as the media target; if it is used as a fallback, it must call `--send-media` with the generated path or URL. `--watch-media-task` remains available when a concrete task id is already known.

中文说明：文本发送由固定 `--send-story` 入口处理；媒体补发由 wrapper 后台 `--watch-recent-media-task` 自动处理，不依赖模型在媒体工具返回后继续执行。原生 completion 即使回来，也不能把 current chat 当作目标。

## Verification

Before declaring setup or upgrade complete:

1. Run `python3 scripts/validate_release.py --root <SKILL_DIR> --config <CONFIG> --skip-smoke`.
2. Read the live job and confirm `payload.kind = command`, exact wrapper argv, bounded timeout/output, `sessionTarget = isolated`, and `delivery.mode = none`.
3. Ensure `day-schedule.md` has a current event, or create a temporary validated schedule for testing.
4. Run `python3 scripts/companion_presence_tick.py --config <CONFIG> --dry-run`.
5. Confirm dry-run output is `would_start_agent` for a matched event or `skip` when no event is active.
6. Confirm prepare output does not expose private paths, channel ids, account ids, session ids, `render_spec`, or top-level `primary_goal`.
7. Run one controlled presence delivery.
8. Confirm the owner saw exactly one message.
9. Confirm the next tick in the same event returns a quiet skip.
10. For a media event, run a controlled watcher test: confirm text sends first, state commits after text delivery, media generation starts, the wrapper records a background watcher pid/log, watcher log ends with `media_task_sent`, and any native completion does not become the only correct-channel delivery path.
