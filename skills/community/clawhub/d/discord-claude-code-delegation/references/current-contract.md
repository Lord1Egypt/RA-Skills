# Current contract

## Roles

- **Operator**: human requester
- **Controller bot**: OpenClaw Discord bot that receives the DM and posts worker tasks
- **Worker bot**: Claude Code Discord bot that consumes the worker lane and returns results

## Required surfaces

You need all of these:

- one controller DM
- one private worker lane in a Discord server
- one controller bot present in that lane
- one worker bot present in that lane

## Canonical task envelope

```text
[WORKER_TASK]
from: Controller Discord DM
source-channel-id: <original-dm-channel-id>
source-message-id: <original-dm-message-id>
requester-discord-id: <requester-discord-id>
task:
@WORKER_BOT <worker-facing task body>
```

## Recommended worker replies

Preferred lane replies:

```text
[WORKER_STATUS] started
source-channel-id: <original-dm-channel-id>
source-message-id: <original-dm-message-id>
requester-discord-id: <requester-discord-id>
task: <short preview>
```

```text
[WORKER_DONE]
source-channel-id: <original-dm-channel-id>
source-message-id: <original-dm-message-id>
requester-discord-id: <requester-discord-id>
result:
<final answer body>
```

## Expected DM result

```text
WorkerBot:
<final answer body>
```

## Closed-loop definition

A working closed loop is:

```text
controller DM -> worker lane -> Claude Code worker -> worker lane -> controller DM
```
