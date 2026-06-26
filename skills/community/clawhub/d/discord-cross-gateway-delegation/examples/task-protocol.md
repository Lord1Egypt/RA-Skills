# Task Protocol Examples

## Dispatch

```text
[KAI_TASK]
id: TASK-20260318-0315-handshake
from: ControllerBot
priority: normal
type: ops
repo: $WORKSPACE_ROOT
goal: Verify that cross-gateway delegation works between the controller bot and the worker bot
instructions:
- Reply with a structured [KAI_STATUS] message
- Confirm you can receive delegated work from the controller bot
- Return one short capability summary of what you can execute on this machine
constraints:
- No destructive actions
- No config changes
- No credential disclosure
deliverables:
- [KAI_STATUS] started or done
```

## Status

```text
[KAI_STATUS]
id: TASK-20260318-0315-handshake
state: done
summary: Worker bot received the task and is ready
artifacts:
- none
blocker: none
next: waiting for the first real delegated task
```

## Completion

```text
[KAI_DONE]
id: KAI-20260318-0400-browser-check
result:
- Verified login page load
- Confirmed no destructive action was taken
artifacts:
- screenshot.png
- https://example.com/login
verification:
- page loaded
- safe boundary respected
follow-up:
- ready for credential-step check if approved
```

## DM fallback note

If private-channel automation fails but DM works, reuse the same protocol in DM without changing the message structure.
