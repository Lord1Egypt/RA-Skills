# Setup Checklist

## Goal

Connect two OpenClaw Discord bots across different gateways so one bot can delegate tasks to the other.

This checklist only covers the setup foundation.
For the complete operating loop (DM trigger -> lane intake -> lane result -> DM relay-back), also read `full-process.md`.

## Proven setup sequence

### 1. Create a private delegation channel

Recommended name:

- `controller-delegation`
- or `<worker-name>-delegation`

Why private:

- keeps task traffic isolated
- protects logs and internal ops messages
- avoids polluting normal chat channels

### 2. Invite the delegating bot into the target server

The bot must exist in the server before any channel permission changes matter.

### 3. Add the bot to the private channel

Important lesson:
Selecting the bot/member in Discord is **not enough**.
You must click the final **save / done** button in the permission modal, or the access is not actually applied.

### 4. Send a handshake task

Example:

```text
[KAI_TASK]
id: KAI-YYYYMMDD-HHMM-handshake
from: ControllerBot
priority: normal
type: ops
repo: <path>
goal: Verify that cross-gateway delegation works
instructions:
- Reply with a structured [KAI_STATUS] message
- Confirm you can receive delegated work
- Return one short capability summary
constraints:
- No destructive actions
- No config changes
- No credential disclosure
deliverables:
- [KAI_STATUS] started or done
```

### 5. Run the 3-stage test matrix

#### Test A — visibility

Confirm the worker side can:

- see the private channel
- see the controller bot messages

#### Test B — DM test

Send a DM from a human operator to the worker bot.
If DM replies work, the worker bot and gateway are alive.

#### Test C — channel mention test

Mention the worker bot in the private channel.
If DM works but channel mention does not, the problem is almost certainly guild/server-channel inbound policy.

## Recommended decision tree

### Case 1: channel works

Use private channel delegation.

### Case 2: DM works, channel fails

Use **DM fallback** now.
Later fix channel policy on the worker gateway.

### Case 3: DM also fails

Investigate worker gateway health, token, inbound processing, or global allow policy first.
