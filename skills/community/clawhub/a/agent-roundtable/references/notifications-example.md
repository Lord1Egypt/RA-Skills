# Real-time Notifications Reference (v2.1+)

Roundtable dispatches discussion lifecycle notifications (`round_start`, `speech`, `round_end`, `concluded`) through configured channels or webhooks when enabled.

## Mode 1: Automatic Notifications (Recommended)

Pass `notifications` when initializing a discussion (`roundtable_init` on Hermes or `RoundtableCore.create_discussion` / `Roundtable.init` in Python).

```python
roundtable_init(
    topic="Synthetic service migration review",
    participants=[
        {"profile": "product", "role": "Product Owner", "perspective": "User impact and scope"},
        {"profile": "engineering", "role": "Tech Lead", "perspective": "Architecture and migration risk"},
        {"profile": "ops", "role": "Operations", "perspective": "Deployment and support load"},
    ],
    max_rounds=3,
    notifications={
        "enabled": True,
        "channels": [{"platform": "feishu", "chat_id": "oc_synthetic_channel_id"}],
        "events": ["round_start", "speech", "round_end", "concluded"],
    },
)
```

### Runtime Behavior

- **Hermes adapter (`roundtable.adapters.hermes`)**: Automatically wires an asynchronous notification sender (`_hermes_send_fn`) that delivers `feishu` channel messages via `~/.hermes/scripts/feishu-send.py` using `HERMES_PROFILE` (default `"default"`). Failures are logged and never block discussion recording.
- **Python / Generic callers**: Supply `send_fn(platform, chat_id, message)` when constructing `RoundtableCore` or `Roundtable`, or configure Discord / Slack URLs via `notifications["webhooks"]` (`roundtable.WebhookSender`).
- **Rule**: NEVER send manual duplicate messages to a channel for events already enabled in `notifications["events"]`.

## Mode 2: Manual Event Trigger or Custom Host Messaging

When `notifications` is omitted or only specific milestones should be pushed manually by an authorized host:

- Use `roundtable_notify(discussion_id="rt_...", event="concluded", conclusion="...")` (Hermes / Python Core) to re-send or manually trigger an event through the configured sender.
- Keep notification channel IDs synthetic in docs/tests and verify user authorization before writing to any external chat.

## Recommended Review Flow with Notifications

1. Coordinator imports materials (`roundtable_add_material`), sets `evidence`, and posts the shared brief in round `0` (`roundtable_speak(participant="coordinator", ...)`).
2. Host runs independent first-pass analyses in parallel (separated contexts, same `context_revision`) and records each speech in turn.
3. Subsequent response rounds focus only on decision-changing conflicts and updated brief revisions.
4. Coordinator submits a structured `report` (or `conclusion`) via `roundtable_end`, keeping recommendations explicitly separate from user-confirmed decisions (do NOT invent numerical confidence indices).
