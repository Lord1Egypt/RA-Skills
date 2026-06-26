# Roundtable Notification send_fn Issue

## ✅ RESOLVED (2026-05-21)

Fix applied in commit `3f9f356`. See `send_fn_fix.md` for the full fix log.

The adapter now passes `_hermes_send_fn` to `RoundtableCore`, which calls
`feishu-send.py` via subprocess. Profile defaults to `HERMES_PROFILE` env var
(default: `default`).

## Key Files
- `src/roundtable/notify.py` — Notifier class (framework-agnostic)
- `src/roundtable/core.py` — RoundtableCore with `_make_notifier()` and `set_send_fn()`
- `src/roundtable/adapters/hermes.py` — Hermes adapter (FIXED)
