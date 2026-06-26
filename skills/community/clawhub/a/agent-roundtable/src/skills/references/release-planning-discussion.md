# Release Planning Discussion Example

**Date**: 2026-05-21
**Discussion ID**: rt_xxxxxxxx
**Topic**: 圆桌(Roundtable)开源发布方案与最新版本测试评估

## Setup

- **Participants**: 饼哥(产品总监), 像素姐(设计师), 码飞(开发工程师)
- **Rounds**: 3 (Round 0 opening + Round 1 initial views + Round 2 deep dive + Round 3 final positions)
- **Duration**: ~8 minutes total (3 delegate_task calls per round, ~20-50s each)

## Workflow

1. `roundtable_init` with 3 participants, `speech_order="fixed"`
2. Coordinator opening statement via `roundtable_speak(participant="coordinator")`
3. Round 1: sequential `delegate_task` to each participant (饼哥 → 像素姐 → 码飞)
4. Coordinator summary via `roundtable_speak(participant="coordinator")`
5. Round 2: same sequential pattern
6. Round 3: same pattern
7. `roundtable_summarize` to get structured data
8. Write conclusion document manually to file
9. `roundtable_end` with brief conclusion text

## Key Pattern: Release Planning Discussion

This discussion type works well for cross-functional alignment before a major milestone.

### Effective participant roles for release planning:
- **Product**: target users, positioning, go-to-market strategy, timeline ownership
- **Design**: visual identity, documentation UX, brand consistency
- **Dev**: code quality, test coverage, CI/CD, technical debt, risk assessment

### What made this discussion productive:
1. **Each round built on previous round's points** — 饼哥修正了自己的"直接发正式版"观点，支持码飞的a1预发布策略
2. **Concrete action items with owners and deadlines** — 10+ items with D1-D24 timeline
3. **Risk identification came from the domain expert** — 码飞 identified test coverage gap (55%→70%)
4. **No major disagreements** — all three converged on the same release path

## Conclusion Document Structure

```markdown
# 圆桌结论：[Topic]

## Summary
- Participants, rounds, date, discussion ID

## 共识点
### 1. [Major decision area]
### 2. [Timeline/milestones]
### 3. [Quality gates]
### 4. [Strategy]

## 分歧点
(Or "无重大分歧" if none)

## 行动项
| # | 行动项 | 负责人 | 截止日期 | 交付物 |

## 风险预警

## 详细发言记录
(Reference to full discussion)
```

## Timing Data

| Phase | Duration | Notes |
|-------|----------|-------|
| roundtable_init | ~1s | Instant |
| Round 1 (3 participants) | ~95s | 22-38s per participant |
| Round 2 (3 participants) | ~133s | 36-50s per participant (longer due to reading history) |
| Round 3 (3 participants) | ~215s | 22-165s per participant (history grew significantly) |
| roundtable_summarize | ~1s | Returns raw JSON |
| Conclusion doc write | ~5s | Manual write_file |

**Total**: ~8 minutes for 3-round, 3-participant discussion.

## Lessons Learned

1. **History reading grows expensive** — Round 3's first participant took 165s because `roundtable_read` returned the full 9-speech history. For longer discussions, consider using `compact=true` in summarize.
2. **Conclusion doc must be written separately** — `roundtable_end` only takes a brief text string. The coordinator must write the full conclusion document as a separate file before or after ending.
3. **Round numbering in summarize output** — The summarize output labels speeches as "Round 0", "Round 1", "Round 2" even though the coordinator called them Round 1, Round 2, Round 3. The actual round tracking in the DB may differ from the coordinator's mental model.
4. **No convergence metrics in summarize** — The `final_convergence_score` was null. Convergence tracking is unreliable; the coordinator should manually assess convergence from discussion content.
