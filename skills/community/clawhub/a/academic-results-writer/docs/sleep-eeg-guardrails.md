# Sleep EEG Guardrails — Full Specification

Moved from main SKILL.md §6.10 and §19.8.

## Pre-Post Sleep Wording Guardrail

When user provides pre-sleep vs post-sleep results but does NOT provide wake control, sleep deprivation control, or randomized sleep vs wake manipulation:

❌ **Prohibited:**
- "睡眠促进……" / "睡眠导致……提高" / "睡眠巩固……"
- "Sleep enhanced …" / "Sleep led to …" / "Sleep consolidated …"

✅ **Recommended:**
- "睡后正确率提高……"
- "从睡前到睡后的提升主要出现在……"
- "该结果与睡眠相关的记忆变化一致，但具体机制应在 Discussion 中讨论。"
- "Post-sleep accuracy was higher than pre-sleep accuracy …"
- "The improvement from pre- to post-sleep was primarily observed in …"

## EEG–Behavior Correlation Wording Guardrail

When EEG–behavior correlation is significant in one condition but not another, AND Fisher r-to-z comparison is significant:

❌ **Prohibited:**
- "该关联仅出现在 A 条件下"
- "B 条件下不存在该关联"
- "该关联具有条件特异性" (without Fisher z)

✅ **Recommended:**
- "该相关在 A 条件下达到显著水平，而在 B 条件下未达到显著水平；Fisher r-to-z 比较进一步显示，两种条件下的相关强度存在显著差异。"
- "该相关模式在不同条件下存在差异，Fisher z = xx, p = xx。"

## Sleep-Control Design Wording Rule

When user does NOT provide wake control, sleep deprivation control, or sleep-vs-wake manipulation, default to:
- "睡前至睡后行为变化" / "pre-to-post behavioral change"
- "睡前至睡后正确率提升" / "pre-to-post change in accuracy"

❌ Default-avoid: "睡后记忆提升" / "overnight memory improvement" / "睡眠相关记忆提升"

**Exception:** Only allow these terms when user explicitly provides sleep-control design or explicitly requests the wording.

## EEG–Behavior Wording Reinforcement for Target-Paper Mode

In target-paper mode, the EEG–behavior correlation guardrail must also be enforced in:
- 【可直接使用的结果段】
- 【可选替代表达】

If wording uses "仅/只/不存在于/特定关联", output must be flagged as failing and corrected.

## Missing Control Wording Rule

When user does not provide control-group design information in the current round:

❌ Do NOT write: "无 wake control" / "没有 sleep control" / "本实验缺少清醒对照组"

✅ Write: "本轮输入未提供 wake control / sleep-vs-wake control 信息" / "在未提供该设计信息的情况下，不宜写'睡眠促进/巩固/导致'。"

**Rule:** Skill can only judge "not provided in current input" — cannot assert that the study lacks a particular design element.
