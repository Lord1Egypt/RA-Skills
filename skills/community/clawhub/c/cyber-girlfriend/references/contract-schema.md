# Turn Contract

`scripts/companion_presence_tick.py` is the default presence automation entrypoint. New OpenClaw installations invoke it directly with an exact argv command payload; the wrapper runs `companion_run.py` for fresh prepare, exits quietly on skip, and starts a fresh dispatch-scoped companion session only when a current event is matched.

## Prepare Stage

Command:

```bash
python3 <SKILL_DIR>/scripts/companion_run.py --stage prepare --config <CONFIG> --no-record-pending
```

Automation command payload:

```json
{
  "kind": "command",
  "argv": [
    "python3",
    "<SKILL_DIR>/scripts/companion_presence_tick.py",
    "--config",
    "<CONFIG>"
    ],
    "cwd": "<SKILL_DIR>",
    "env": {
      "PYTHONUNBUFFERED": "1"
    },
    "timeoutSeconds": 120,
  "outputMaxBytes": 65536
}
```

Prepare selects the current `day-schedule.md` event by real local time. Events marked `必定发生：是` are life facts, not guaranteed sends.

Required output fields:
- `status`
- `run_id`
- `life_context`
- `delivery_contract`
- `media_contract`
- `state_commit`
- `next_step`

`life_context` is structured and must contain:
- `generated_at`
- `timezone`
- `speaker`
- `today`
- `event`
- `reality_check`

Optional:
- `delivery_mood`

The tick wrapper passes the prepared contract to a fresh dispatch-scoped companion session when status is ok. That session writes one first-person companion presence story directly from `life_context`. There is no separate render stage and no `render_spec` in the current architecture. A prepared run id is appended to the configured base session key, so an archived session from an earlier event is never resumed.

Prepare output must not include duplicated task fields or local-only execution hints:
- no top-level `primary_goal`
- no `render_spec`
- no local runbook fields
- no private local paths or channel identifiers beyond the configured delivery contract

Agents should not infer delivery ownership from prose. Follow these fields:
- `delivery_contract.send_in_main_turn = true`: text may be sent in the main turn.
- `media_contract.kind = event_media`: the current event requires media.
- `media_contract.async = true`: OpenClaw media generation is asynchronous.
- `media_contract.tool_name`: the runtime-selected async media generator for the matched media type.
- `media_contract.completion_event_is_sender = true`: the media task is asynchronous and will produce a native OpenClaw completion event.
- `media_contract.callback_context.strategy = same_stable_session`: "stable" means the same dispatch-scoped session for the lifetime of this one media task, not a session reused across events.
- `media_contract.callback_context.requires_original_session_context = true`: the completion turn relies on that dispatch session context to keep the original delivery contract available.
- `state_commit.when`: defines when pacing state can be committed.

The presence agent must send text through `companion_presence_tick.py --send-story --story-stdin`, not through the runtime `message(action="send")` tool. `--send-story` reloads the saved contract from the dispatch lock, sends the text presence story with the explicit `delivery_contract`, and runs `state_commit.command` only after visible text delivery succeeds.

`life_context.event.media_info` may describe a concrete photo, audio, video, or similar media artifact for the matched event. If present, the presence agent calls the selected async media generation path only after `--send-story` succeeds. The wrapper also starts `companion_presence_tick.py --watch-recent-media-task` for the dispatch session; that helper finds the next media task created after launch, waits for generated media paths, and sends with the explicit `delivery_contract`. If the native media completion later returns to the same dispatch session, it may only use `companion_presence_tick.py --send-media` as a fallback and must not run `state_commit.command` again.

中文说明：正文主路径是固定 `--send-story` 入口，媒体补发主路径是 wrapper 自动启动的 `--watch-recent-media-task`。两者都不能让模型自己判断 current/original chat；completion 兜底也只能调用固定 `--send-media` 入口。

For both media events and text-only events, `state_commit.when = after_text_send`. Media success is a follow-up enhancement, not the event completion gate.

`media_contract` stays intentionally generic. It must not carry local runbook paths, private workspace details, or user-specific media instructions.

Use `assets/turn-contract.schema.json` for machine validation.
