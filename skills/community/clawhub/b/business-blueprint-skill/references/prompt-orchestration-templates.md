# Prompt Orchestration Templates

Use these templates when an agent platform chains `kai-business-blueprint`, `kai-report-creator`, and `kai-slide-creator` through prompts instead of CLI flags.

## Principles

1. `solution.blueprint.json` is the upstream semantic source.
2. `solution.projection.json` is the canonical downstream-friendly machine projection.
3. `solution.handoff.json` is only a viewer manifest. Do not use it as report/deck input.
4. Report and slide should stop at their native planning artifacts first:
   - report -> `.report.md`
   - slide -> `PLANNING.md`
5. If the projection does not exist yet, create it before prompting downstream skills.

## Recommended Flow

```text
raw notes / workshop transcript
  -> business blueprint
  -> solution.blueprint.json
  -> solution.projection.json
  -> report IR or deck plan
  -> final report HTML or slide HTML
```

## Template 1: Blueprint Generation

Use this when the upstream skill is turning raw materials into a blueprint.

```text
请基于以下材料生成 business blueprint。

要求：
- 输出 canonical `solution.blueprint.json`
- 不要输出给人读的 handoff 文档
- 如果材料信息不足，把问题写进 `context.clarifyRequests`
- 行业使用最接近的一个：common / finance / manufacturing / retail

源材料：
[粘贴会议纪要、售前材料、方案草稿或访谈记录]
```

English variant:

```text
Generate a business blueprint from the materials below.

Requirements:
- Output canonical `solution.blueprint.json`
- Do not create a human-readable handoff document
- If information is missing, write the gaps into `context.clarifyRequests`
- Choose exactly one closest industry: common / finance / manufacturing / retail

Source material:
[paste notes, presales input, workshop transcript, or solution draft]
```

## Template 2: Projection Generation

Use this as the internal preparation step before report/slide work if only `solution.blueprint.json` exists.

```text
基于 `solution.blueprint.json` 生成 canonical `solution.projection.json`。

要求：
- 这是给下游 skill 用的 machine projection，不是给人看的摘要
- 保留 goals / scope / assumptions / constraints / openQuestions
- 提炼 keyCapabilities / actors / coreFlows / systems
- 生成 diagnostics.warnings
- 不要写回 blueprint JSON
```

English variant:

```text
Generate canonical `solution.projection.json` from `solution.blueprint.json`.

Requirements:
- This is a machine projection for downstream skills, not a human-facing summary
- Preserve goals / scope / assumptions / constraints / openQuestions
- Extract keyCapabilities / actors / coreFlows / systems
- Emit diagnostics.warnings
- Do not modify the blueprint JSON
```

## Template 3: Report IR From Blueprint

Use this when invoking `kai-report-creator` from the platform.

```text
请基于这个 business blueprint artifact 生成 report IR，先不要生成 HTML。

输入：
- blueprint: `solution.blueprint.json`
- projection: `solution.projection.json`

要求：
- 优先读取 `solution.projection.json`；只有在核对来源时才参考 blueprint
- 输出 `.report.md`
- 不要编造数字；没有量化数据就不要造 KPI
- 默认章节：
  1. Executive Summary
  2. Business Goals And Scope
  3. Capability Map And Ownership
  4. Core Operational Flows
  5. System Landscape
  6. Assumptions, Constraints, And Open Questions
  7. Recommended Next Actions
- 如果 projection 的 diagnostics 只有 warning 且信息稀疏，输出 skeleton IR，并明确标出 placeholder
```

English variant:

```text
Use this business blueprint artifact to generate a report IR first. Do not render HTML yet.

Inputs:
- blueprint: `solution.blueprint.json`
- projection: `solution.projection.json`

Requirements:
- Read `solution.projection.json` as the primary source; only inspect the blueprint for provenance checks
- Output `.report.md`
- Do not invent numbers; if there is no quantitative data, do not fabricate KPI blocks
- Default sections:
  1. Executive Summary
  2. Business Goals And Scope
  3. Capability Map And Ownership
  4. Core Operational Flows
  5. System Landscape
  6. Assumptions, Constraints, And Open Questions
  7. Recommended Next Actions
- If diagnostics contain only warnings and the projection is sparse, produce a skeleton IR with explicit placeholders
```

## Template 4: Slide Plan From Blueprint

Use this when invoking `kai-slide-creator` from the platform.

```text
请基于这个 business blueprint artifact 生成 deck 的 `PLANNING.md`，先不要生成 HTML。

输入：
- blueprint: `solution.blueprint.json`
- projection: `solution.projection.json`

要求：
- 优先读取 `solution.projection.json`
- 输出 `PLANNING.md`
- 默认使用 8 页 business architecture / transformation arc：
  1. Cover / Transformation Thesis
  2. Current-State Pain
  3. Goals And Scope
  4. Capability Map
  5. Core Business Flow
  6. System Landscape
  7. Design Choices / Target Operating Model
  8. Rollout / Next Steps
- 每页只讲一个主点，不要把原始 graph 生硬塞进一页
- 如果 projection 信息稀疏，保持 8 页结构，但在 speaker note 或 supporting bullets 中明确缺口
```

English variant:

```text
Use this business blueprint artifact to generate `PLANNING.md` for a deck first. Do not generate HTML yet.

Inputs:
- blueprint: `solution.blueprint.json`
- projection: `solution.projection.json`

Requirements:
- Read `solution.projection.json` as the primary input
- Output `PLANNING.md`
- Default to an 8-slide business architecture / transformation arc:
  1. Cover / Transformation Thesis
  2. Current-State Pain
  3. Goals And Scope
  4. Capability Map
  5. Core Business Flow
  6. System Landscape
  7. Design Choices / Target Operating Model
  8. Rollout / Next Steps
- Keep one dominant idea per slide; do not dump the raw graph into a single dense slide
- If the projection is sparse, keep the 8-slide structure but mark the gaps explicitly in notes or supporting bullets
```

## Template 5: Full Report Chain

Use this when the platform orchestrates blueprint -> projection -> report end to end.

```text
你现在要串联 business blueprint 和 report skill。

步骤：
1. 如果 `solution.blueprint.json` 不存在，先根据原始材料生成它
2. 如果 `solution.projection.json` 不存在，先从 blueprint 生成它
3. 基于 projection 生成 `.report.md`
4. 停在 IR 阶段，等待确认；不要直接生成 HTML

约束：
- `solution.handoff.json` 只给 viewer，用不到这里
- 不要把 raw blueprint graph 当成 report 的直接写作输入
- 不要编造任何数字
```

## Template 6: Full Slide Chain

Use this when the platform orchestrates blueprint -> projection -> slide end to end.

```text
你现在要串联 business blueprint 和 slide skill。

步骤：
1. 如果 `solution.blueprint.json` 不存在，先根据原始材料生成它
2. 如果 `solution.projection.json` 不存在，先从 blueprint 生成它
3. 基于 projection 生成 `PLANNING.md`
4. 停在 planning 阶段，等待确认；不要直接生成 HTML

约束：
- `solution.handoff.json` 只给 viewer，用不到这里
- 不要把 raw blueprint graph 直接当成 deck 文案
- 默认使用 8 页 business transformation arc，除非 projection 清楚支持扩展
```

## Template 7: Report + Slide Parallel Planning

Use this when the platform wants both deliverables from the same blueprint.

```text
基于同一个 business blueprint artifact，同时准备 report 和 slide，但都先停在 planning / IR 阶段。

输入：
- blueprint: `solution.blueprint.json`
- projection: `solution.projection.json`

输出：
- report: `.report.md`
- slide: `PLANNING.md`

约束：
- 两者都以 projection 为主输入
- report 偏完整叙述与结构化说明
- slide 偏单页主张与叙事节奏
- 不要互相复制文本；同一事实可以重述，但表现形式要不同
```

## Anti-Patterns

Do not use prompts like these:

```text
Use solution.handoff.json to make a deck
```

Reason: `solution.handoff.json` is only a viewer manifest.

```text
Read the full blueprint graph and directly write final slides
```

Reason: this bypasses the projection layer and mixes semantic extraction with presentation generation.

```text
Generate the report and the final HTML in one step from raw notes
```

Reason: this skips the IR checkpoint and makes review much harder.

## Minimal Platform Recipe

If the platform only needs one compact reusable pattern, use this:

```text
If the input is raw business material:
1. generate `solution.blueprint.json`
2. generate `solution.projection.json`

If the target is report:
3. generate `.report.md` from the projection
4. only after review, render HTML

If the target is slide:
3. generate `PLANNING.md` from the projection
4. only after review, generate HTML

Never use `solution.handoff.json` as report/slide input.
```
