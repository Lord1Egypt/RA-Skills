# Channel Map

Notification routing configuration for the orchestration system.

## Operations Channel

| Channel | ID | Thread | Purpose |
|---------|----|--------|---------|
| Operations | _(set during setup)_ | _(set during setup)_ | System notifications, alerts |

## Task Routing

By default, all task status messages and results are delivered to the channel where the owner sent the request.

For multi-agent or complex tasks, Leader may create a dedicated thread: `message(action: "topic-create", name: "{emoji} {task name}")`.

## Channel Configuration

- **Platform:** _(set during setup)_
- **Mode:** _(set during setup)_
- **Credentials:** Configured in `openclaw.json` (not stored here)
