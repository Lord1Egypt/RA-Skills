# Roundtable Notifications Implementation

## Architecture

```
roundtable_init(notifications={...})
    ↓
discussions table: notifications JSON column
    ↓
roundtable_speak() / roundtable_end()
    ↓
core._make_notifier(disc.notifications) → Notifier(config, send_fn)
    ↓
Notifier.notify(event, ...) → send_fn(platform, chat_id, message)
    ↓
_hermes_send_fn → subprocess → feishu-send.py
```

## Key Files

| File | Role |
|------|------|
| `src/roundtable/notify.py` | Framework-agnostic Notifier class |
| `src/roundtable/core.py` | Business logic, calls notifier on events |
| `src/roundtable/db.py` | SQLite schema with notifications JSON column |
| `src/roundtable/adapters/hermes.py` | Hermes adapter with `_hermes_send_fn` |

## send_fn Wiring (Critical)

The Hermes adapter must pass `send_fn` to `RoundtableCore`:

```python
# adapters/hermes.py
def _hermes_send_fn(platform: str, chat_id: str, message: str) -> None:
    try:
        if platform == "feishu":
            profile = os.environ.get("HERMES_PROFILE", "default")
            script = os.path.expanduser("~/.hermes/scripts/feishu-send.py")
            subprocess.run(
                ["python3", script, profile, chat_id, message],
                capture_output=True, timeout=15,
            )
        else:
            logger.warning("Unsupported notification platform: %s", platform)
    except Exception as e:
        logger.warning("Notification send failed (platform=%s, chat=%s): %s", platform, chat_id, e)

def _get_core() -> RoundtableCore:
    global _core
    if _core is None:
        _core = RoundtableCore(send_fn=_hermes_send_fn)  # ← MUST pass send_fn
    return _core
```

## Execution Flow (Real Sub-Agents)

Each participant is a `delegate_task` call:

```
Coordinator (main agent)
    ↓ roundtable_init(notifications={...})
    ↓ roundtable_speak(participant="coordinator") — opening
    ↓
    For each round:
        ↓ delegate_task to participant 1 (independent sub-agent)
        ↓   → sub-agent calls roundtable_speak(participant="bingge")
        ↓   → core.speak() fires Notifier.notify("speech", ...)
        ↓   → _hermes_send_fn → feishu-send.py → Feishu group
        ↓
        ↓ delegate_task to participant 2 (independent sub-agent)
        ↓   → same flow
        ↓
        ↓ delegate_task to participant 3 (independent sub-agent)
        ↓   → same flow
        ↓
        ↓ roundtable_speak(participant="coordinator") — round summary
    ↓
    roundtable_end(conclusion="...")
    ↓ Notifier.notify("concluded", ...)
```

## Timing

- 4 participants × 4 rounds = 16 delegate_task calls
- Each delegate_task: 10-40 seconds (model inference)
- Total: ~15-20 minutes for a full discussion
- Notifications add ~1-2 seconds per speech (subprocess call)

## Notification Config Schema

```json
{
    "enabled": true,
    "channels": [
        {"platform": "feishu", "chat_id": "oc_xxx"}
    ],
    "events": ["round_start", "speech", "round_end", "concluded"]
}
```

- `enabled`: false → no notifications (default)
- `channels`: list of {platform, chat_id} targets
- `events`: optional, defaults to all 4 events
