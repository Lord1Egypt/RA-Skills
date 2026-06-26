# Revision Mode — Full Specification

Moved from main SKILL.md §18.

## Workflow

1. Mark strengths in the draft
2. Identify missing/incorrect statistics
3. Mark Discussion leakage
4. Mark causal inflation
5. Mark wording too strong/weak
6. Provide revised version
7. Annotate each change with reason

## Output Format

```
【草稿评估】
优点：……
统计问题：……
边界问题：……
措辞问题：……

【修订版】
……（完整修订文段）

【修改说明】
- 第X句：……改为……，原因：……
- 第Y句：……增加到 Discussion，原因：……
```

## Source-Boundary Rule

When revising Results drafts, distinguish three categories of statistical values:

| Source | Can add to revision? | Notes |
|--------|---------------------|-------|
| Values already in user's draft | ✅ Retain and check | If suspicious, mark but don't change unilaterally |
| Values user additionally provides in same round | ✅ Can add | M/SD/F/p/etc. from supplementary data |
| Values from previous rounds, context memory, or similar cases | ❌ Forbidden | Unless user explicitly says "use the statistics from above" |

## Missing-Statistics Handling

**A. Provided, can retain:** "User provided this value in current round; retained and checked."

**B. Not provided this round, not added:** "User did not provide this value in current round; placeholder kept or reminder added."

**C. Partially provided, needs confirmation:** "Draft contains [existing info] but lacks [missing info]. Revision retains existing content; recommend user supplements missing."

## Partial Design Information Rule

When draft has partial design info (e.g., "Schema condition × Time", "repeated-measures ANOVA", "interaction") but doesn't fully provide factor levels or design structure:

Layer the report:
- **Identifiable from draft:** schema condition × time, repeated-measures ANOVA
- **Still missing:** complete factor level names, Chinese variable names, within/between-subjects structure, N

Use Category C labeling in statistical reporting check.

## Missing Control Wording Rule

When user does NOT provide wake/sleep control info in current round:

❌ "无 wake control" / "没有 sleep control" / "本实验缺少清醒对照组"

✅ "本轮输入未提供 wake control / sleep-vs-wake control 信息" / "在未提供该设计信息的情况下，不宜写'睡眠促进/巩固/导致'。"

## Null-Result Warning Placement Rule

Meta-explanations about non-significant results (e.g., "非显著结果不应被解释为两种条件等同") should default to:
- ✅ 【统计报告检查】
- ✅ 【结果与讨论边界提醒】
- ✅ 【修改说明】

NOT default to:
- ❌ 【修订版】/【可直接使用的结果段】formal text

Formal Results section recommends factual statement only: "差异未达到显著水平，t(df) = xx, p = xx。"
