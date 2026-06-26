# Memory Template - Chat Rooom

Create `~/chat-rooom/memory.md` with this structure:

```markdown
# Chat Rooom Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Activation Defaults
<!-- When room mode should activate -->
<!-- Situations where logging should stay minimal -->

## Room Defaults
<!-- Default room names, channels, and role patterns -->

## Durable Preferences
<!-- Preferences about claims, summaries, checkpoints, or room cadence -->

## Repeated Traps
<!-- Failures worth preventing early -->

## Notes
<!-- Stable observations only -->

---
*Updated: YYYY-MM-DD*
```

Create `~/chat-rooom/rooms.md`:

```markdown
# Recent Rooms

## YYYY-MM-DD - [Room Name]
Workspace: ...
Purpose: ...
Participants: ...
Channels: ...
Pattern worth reusing: ...
```

Create `.chat-rooom/rooms/<room>/room.md`:

```markdown
# Room: <room>
Status: active
Goal: ...
Participants: @planner, @builder, @reviewer
Channels: general, build, review
Updated: YYYY-MM-DDTHH:MM:SSZ
```

Create `.chat-rooom/rooms/<room>/summary.md`:

```markdown
# Summary
Status: active | blocked | waiting | done
Decision owner: @agent
Current focus: ...
Latest decision: ...
Open question: ...
Next action: ...
Updated: YYYY-MM-DDTHH:MM:SSZ
```

Create `.chat-rooom/rooms/<room>/jobs.md` and `claims.md` as compact tables. Keep each row to one task or one claimed surface.

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default | Keep learning room defaults |
| `complete` | Stable setup | Use saved patterns with light refresh |
| `paused` | User wants less process | Keep rooming manual |
| `never_ask` | User rejected integration | Stop prompting and stay quiet |
