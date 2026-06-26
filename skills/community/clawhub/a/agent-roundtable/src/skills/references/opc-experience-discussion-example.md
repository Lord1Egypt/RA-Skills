# OPC Experience Discussion — Working Example

**Date**: 2026-05-21
**Discussion ID**: `rt_xxxxxxxx`
**Participants**: 4 (bingge/pixiel/mafei/default)
**Rounds**: 4
**Total duration**: ~15 minutes

## What Worked

1. **Sequential delegation** — Delegating to each participant one at a time allowed them to read previous responses and build on each other's points
2. **Coordinator summarizing between rounds** — After each round, coordinator spoke to synthesize key points, which gave participants context for the next round
3. **Role-specific prompts** — Including persona details (口头禅, speaking style) in the delegate_task context produced character-consistent responses
4. **Structured round themes** — Pre-defining each round's purpose (Round 1: overall evaluation, Round 2: respond/supplement, Round 3: improvement suggestions, Round 4: convergence) kept discussion focused
5. **Parallel delegation for same round** — Delegating to all 3 participants in parallel for each round (via `delegate_task` with `tasks` array) worked when they only needed to read history, not each other's current-round responses

## What Didn't Work

1. **Round tracking** — All speeches recorded as Round 0, had to track manually
2. **summarize output** — 148KB raw JSON, had to write conclusion manually
3. **No roundtable_advance** — Referenced in user prompt but doesn't exist

## Actual Workflow Used

```
1. roundtable_init(topic, context, participants, max_rounds=4)
2. roundtable_speak(participant="coordinator") — opening statement
3. For each round:
   a. delegate_task to each participant (with roundtable toolset)
   b. roundtable_speak(participant="coordinator") — round summary
4. roundtable_summarize() — get raw data
5. Write conclusion document manually
6. roundtable_end(conclusion="...")
```

## Timing

| Phase | Duration |
|-------|----------|
| Round 1 (3 participants) | ~90s |
| Round 2 (3 participants) | ~120s |
| Round 3 (3 participants) | ~260s |
| Round 4 (3 participants) | ~110s |
| Coordinator summaries | ~30s |
| Report writing | ~30s |
| **Total** | **~11 min** |

## Key Learnings

- 4 participants × 4 rounds = 16 delegate_task calls. Plan for ~15 minutes.
- Each participant needs 30-60 seconds per round.
- The coordinator's between-round summaries are critical for discussion quality.
- Write the conclusion report yourself — summarize gives you raw data, not insights.
