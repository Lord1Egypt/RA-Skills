# AI Relay Iteration Discussion — Working Example with Notifications

**Date**: 2026-05-21
**Discussion ID**: `rt_xxxxxxxx`
**Participants**: 4 (bingge/pixiel/mafei/default)
**Rounds**: 4
**Total duration**: ~20 minutes
**Notifications**: Pushed to company group `oc_your_company_group_id`

## What Made This Discussion Effective

1. **Pre-built context** — Coordinator created a rich `context` in `roundtable_init` describing the current AI Relay state, tech stack, and constraints. This gave all participants a shared baseline.

2. **Round themes** — Each round had a clear purpose:
   - Round 1: Initial positions from each role
   - Round 2: Focus on disagreements (KV vs Postgres, Streaming priority, billing timing)
   - Round 3: Final positions + Sprint roadmap
   - Round 4: Closing statements + confidence index

3. **Coordinator summaries between rounds** — After each round, coordinator called `roundtable_speak(participant="coordinator")` to synthesize key points. This gave participants context for the next round and kept the discussion focused.

4. **Manual notification pattern** — Since send_fn was not yet wired, coordinator manually called `send_message` after each speech:
   ```python
   # After each delegate_task returns:
   send_message(
       target="feishu:oc_your_company_group_id",
       message=f"💬 圆桌讨论 [rt_xxxxxxxx] 第{N}轮 | {角色}（{职位}）发言：\n{摘要}"
   )
   ```

5. **Project positioning correction** — Boss corrected the project scope AFTER the discussion (personal/open-source, not commercial). The coordinator updated the conclusion document accordingly. **Lesson**: confirm project constraints BEFORE the discussion if possible.

## Timing

| Phase | Duration | Notes |
|-------|----------|-------|
| Round 1 (3 participants) | ~55s | 饼哥 15s + 像素姐 16s + 码飞 22s |
| Round 2 (3 participants) | ~80s | Longer due to roundtable_read (context growing) |
| Round 3 (3 participants) | ~100s | Even longer — summarize context is ~150KB |
| Round 4 (3 participants) | ~35s | Shorter — final statements |
| Coordinator summaries | ~20s | |
| Conclusion writing | ~10s | |
| **Total** | **~5 min active** | ~20 min wall with notifications |

## Key Learning: Context Size Growth

Each round, the `roundtable_read` context grows significantly:
- Round 1: ~5K input tokens
- Round 2: ~8K input tokens
- Round 3: ~130K input tokens (raw JSON from roundtable_read!)
- Round 4: ~5K input tokens (coordinator passes summary, not full history)

**Mitigation**: In Round 3-4, pass a coordinator-written summary instead of `roundtable_read` output to keep context manageable.

## Output
- Conclusion document: `/Users/parsifal/Repo/Service/ai-relay/docs/AI-RELAY-ITERATION-PLAN.md`
- Notifications: 10+ messages pushed to company group (open, per-speech, round-end, concluded)
