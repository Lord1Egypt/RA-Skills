# Secondary Worker Rollout

## Objective

Use a second OpenClaw bot as a worker for MAI Universe-style multi-project task splitting.

## Recommended role

Default recommendation:

- **Main bot** = control tower
- **Secondary bot** = worker / execution lane

For real delegated work, the main bot should usually act as an orchestrator first: understand the user's request, generate the worker-facing prompt/envelope, then hand the task to MACJini. Keep raw worker-prefix shortcuts available, but treat them as fast paths rather than the preferred operating model for important work.

## Work split recommendation

### Keep on the main bot

- conversation with the operator
- orchestration and routing
- final decision making
- memory updates
- cron ownership when possible
- multi-project priority management

### Push to the secondary bot

- browser-heavy tasks
- long-running research
- platform-specific validation work
- web workflows that should not block the main session
- delegated execution tasks with clear deliverables

## Best transport choices

### Preferred end-state

Private Discord delegation lane in a server channel.

Recommended lane name:

- `#worker-delegation`
- or `#<worker-name>-delegation`

For MACJINI specifically, the proven lane name is:

- `#macjini-delegation`

Recommended protocol namespace for this lane:

- `[MAC_TASK]`
- `[MAC_STATUS]`
- `[MAC_DONE]`

### Temporary fallback

If the secondary bot works in DM but not in server channels, use **DM-based delegation** until the worker-device config is updated.

## Secondary-bot decision tree

### If DM works and channel does not

- inspect guild/server-channel policy on the worker device
- with `groupPolicy: allowlist`, add the target guild/channel to `guilds`
- do not consider setup complete until a channel-based `[KAI_STATUS]` arrives

### If both DM and channel work

- switch to private channel delegation as the standard mode

### If neither works

- inspect worker gateway health first

## Proven completion pattern

The following configuration pattern successfully enabled channel-based delegation for a secondary bot:

- `groupPolicy: allowlist` retained
- target guild added to `guilds`
- target private channel added under the guild allowlist
- gateway reloaded/restarted
- channel-based `[KAI_STATUS]` verified from the worker bot

## First practical delegated task types

1. Browser automation handoff
2. Long web research handoff
3. Platform-specific validation
4. Repetitive monitoring tasks with structured outputs

## Suggested first real delegated task

```text
[KAI_TASK]
id: WORKER-YYYYMMDD-HHMM-first-task
from: ControllerBot
priority: normal
type: research
goal: Verify delegated execution path and return a structured summary
instructions:
- Do one bounded task only
- Return [KAI_STATUS] first, then [KAI_DONE]
deliverables:
- short result
- artifact list
```
