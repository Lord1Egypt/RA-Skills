# Notification Debugging Guide

## Verifying Messages Arrived (Critical Pitfall)

The Feishu Messages API returns messages in **chronological order** (oldest first)
by default. When verifying notifications arrived, always use `sort_type=ByCreateTimeDesc`:

```python
resp = requests.get(
    'https://open.feishu.cn/open-apis/im/v1/messages',
    params={
        'receive_id_type': 'chat_id',
        'container_id_type': 'chat',
        'container_id': 'oc_xxx',
        'page_size': 20,
        'sort_type': 'ByCreateTimeDesc'  # ← CRITICAL
    },
    headers={'Authorization': f'Bearer {token}'}
)
```

Without `sort_type=ByCreateTimeDesc`, the API returns the oldest messages first,
which makes it look like notifications never arrived. This caused a 30-minute
false debugging session on 2026-05-23.

## Debug send_fn Wrapper

If notifications appear to not fire, wrap `send_fn` with logging:

```python
original_send = roundtable_tools._hermes_send_fn

def debug_send_fn(platform, chat_id, message):
    print(f"[DEBUG SEND] platform={platform}, chat={chat_id}, msg_len={len(message)}")
    try:
        original_send(platform, chat_id, message)
        print(f"[DEBUG SEND] OK")
    except Exception as e:
        print(f"[DEBUG SEND] FAILED: {e}")

core = RoundtableCore(send_fn=debug_send_fn)
```

## Checklist When Notifications Don't Appear

1. **Check API sort order** — Use `sort_type=ByCreateTimeDesc` (see above)
2. **Verify send_fn is wired** — `core._send_fn is not None`
3. **Verify notifications config** — Check DB: `SELECT notifications FROM discussions WHERE id='rt_xxx'`
4. **Verify notifier.enabled** — `notifier.enabled` should be `True`
5. **Check HERMES_PROFILE** — Defaults to `"default"`, must match a valid profile
6. **Check feishu-send.py** — Run manually: `python3 ~/.hermes/scripts/feishu-send.py default oc_xxx "test"`

## Multiple roundtable.db Files

The system may have multiple databases — verify against the correct one:
- `~/.roundtable/roundtable.db` — main agent discussions
- `~/.hermes/roundtable.db` — hermes tool layer discussions
- `~/.hermes/profiles/{profile}/home/.roundtable/roundtable.db` — sub-agent discussions
