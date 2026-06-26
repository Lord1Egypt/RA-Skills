# Notification send_fn Wiring — Fix Log

## Problem
The Hermes adapter (`adapters/hermes.py`) created `RoundtableCore()` without passing
a `send_fn`, so notifications configured in `roundtable_init` were silently ignored.

## Root Cause
```python
# BEFORE (broken):
def _get_core() -> RoundtableCore:
    global _core
    if _core is None:
        _core = RoundtableCore()  # No send_fn!
    return _core
```

The `Notifier.enabled` property returns `False` when `send_fn is None`.

## Fix (2026-05-21)
Added `_hermes_send_fn` callback in `adapters/hermes.py`:

```python
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

# AFTER (fixed):
def _get_core() -> RoundtableCore:
    global _core
    if _core is None:
        _core = RoundtableCore(send_fn=_hermes_send_fn)
    return _core
```

## Key Details
- Uses `subprocess.run` to call `feishu-send.py` (avoids import dependency on Hermes internals)
- `HERMES_PROFILE` env var controls which bot profile sends messages (default: `default`)
- All exceptions caught and logged — never blocks discussion flow
- 15-second timeout on subprocess call
- Only supports `feishu` platform currently; others log a warning

## Verification
```python
from roundtable.adapters.hermes import _hermes_send_fn, _get_core
core = _get_core()
assert core._send_fn is not None  # True
assert core._send_fn is _hermes_send_fn  # True
```

## Commits
- `3f9f356` fix(roundtable): connect send_fn in Hermes adapter for notification delivery
- `d8ae331` fix: default HERMES_PROFILE to 'default' instead of 'mafei'
