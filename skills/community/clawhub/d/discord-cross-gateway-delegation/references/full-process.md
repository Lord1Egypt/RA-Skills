# Full process

## Goal

Move this skill from "channel setup" to a full delegation operating model.

A complete cross-gateway delegation rollout is only done when all of the following work:

1. controller bot can auto-create a worker task
2. worker bot can accept the task in the private lane
3. worker bot can post started/final status in the lane
4. controller bot can relay the final result back into the original DM

## Canonical end-to-end flow

### 1. Human speaks to the controller bot in DM

Example:

```text
maekjini, check the Safari login flow again
```

### 2. Controller bot rewrites the DM into a structured task envelope

Example MACJINI envelope:

```text
[MAC_TASK]
from: MAIJini Discord DM
source-channel-id: <dm-channel-id>
source-message-id: <dm-message-id>
requester-discord-id: <user-id>
task:
Check the Safari login flow again
```

### 3. Controller bot posts the envelope into the worker lane

Example lane:

- `#macjini-delegation`

### 4. Worker bot accepts the lane task

Expected started reply:

```text
[MAC_STATUS] started
source-channel-id: <dm-channel-id>
source-message-id: <dm-message-id>
requester-discord-id: <user-id>
task: <short preview>
```

### 5. Worker bot posts a final result

Expected final reply:

```text
[MAC_DONE]
source-channel-id: <dm-channel-id>
source-message-id: <dm-message-id>
requester-discord-id: <user-id>
result:
<final worker answer>
```

### 6. Controller bot relays the final result back to the original DM

Recommended DM format:

```text
WorkerName:
<final worker answer>
```

When possible, send this as a reply to the original DM message id.

## Success criteria

The rollout is successful only when:

- the worker lane receives the task
- the worker lane produces started/final output
- the original DM receives the final worker result

Anything short of DM result relay-back is only partial success.

## Trigger design

Natural-language DM triggers should stay narrow, but they can support two modes.

### Quick handoff

Examples:

- `maekjini ...`
- `maekjiniya ...`
- `kaijini ...`

Use this for short tasks and simple tests.

### Orchestrated handoff (preferred for real work)

Examples:

- `MAIJini, send this to MACJini: ...`
- `MAIJini, have MACJini verify this browser flow`
- `MAIJini, delegate this task to MACJini`

Use this when the controller bot should interpret the task first, create a richer worker-facing envelope, and remain the obvious control tower.

Rules:

- DM only
- owner/operator scope only when possible
- non-matching DM messages must continue through the normal conversation path
- full success still requires final DM relay-back

## Lane-specific protocol naming

Use worker-specific protocol names to reduce confusion.

Examples:

- MACJINI lane -> `MAC_*`
- KAIJINI lane -> `KAI_*`

Legacy compatibility is acceptable during migration, but the skill should recommend matching the worker identity.

## Relay-back rule

The final worker answer should be relay-friendly.

Preferred forms:

1. a `[WORKER_DONE]` envelope with `source-channel-id` and `source-message-id`
2. a natural-language reply that references the original task message or the worker started message

The controller should ignore noisy intermediate updates in the original DM.

Recommended policy:

- do not relay `started` acknowledgements into the DM
- relay final answers only

## Proven troubleshooting split

### Case A — DM trigger fails

Problem area:

- controller-side auto-delegation

### Case B — task reaches lane but worker does not respond

Problem area:

- worker-side preflight / bot-message gating / guild policy

### Case C — worker responds in lane but not in DM

Problem area:

- controller-side result bridge / correlation / reply metadata

## Recommended implementation boundaries

Keep the behavior narrow:

- hard-coded or explicit worker lane ids are acceptable
- require structured envelopes
- reject empty task bodies
- avoid broad cross-channel bot exceptions
- keep reply/relay behavior isolated to the dedicated worker lane
