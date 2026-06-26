# Example envelopes

## Canonical task envelope

```text
[WORKER_TASK]
from: Controller Discord DM
source-channel-id: <original-dm-channel-id>
source-message-id: <original-dm-message-id>
requester-discord-id: <requester-discord-id>
task:
@WORKER_BOT Summarize this link in one paragraph.
```

## Relay-friendly final envelope

```text
[WORKER_DONE]
source-channel-id: <original-dm-channel-id>
source-message-id: <original-dm-message-id>
requester-discord-id: <requester-discord-id>
result:
Done. Here is the one-paragraph summary.
```

## Expected DM result

```text
WorkerBot:
Done. Here is the one-paragraph summary.
```
