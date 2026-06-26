---
"name": "cocoloop-graduate-defense-ppt"
"description": "帮助用户制作研究生毕业答辩 PPT，并提供稳定的设计背景与页级内容结构"
"version": "0.1.0"
"author": "tanshow"
"generated_by_cocoloop": true
"when_to_use": "帮助用户制作研究生毕业答辩 PPT，并提供稳定的设计背景与页级内容结构. Typical scenarios: 生成毕业答辩 PPT 结构; 确定答辩页面视觉方向; 整理答辩讲稿与实验结果"
"user-invocable": true
---
# Graduate Defense PPT

## Overview

帮助用户制作研究生毕业答辩 PPT，并提供稳定的设计背景与页级内容结构

## Use Cases

- 生成毕业答辩 PPT 结构
- 确定答辩页面视觉方向
- 整理答辩讲稿与实验结果

## Inputs

- `thesis_topic`: 论文题目或答辩主题
- `research_materials`: 实验结果、图表、结论与摘要材料

## Outputs

- `defense_outline` (markdown): 答辩 PPT 大纲
- `visual_design_input` (markdown): 默认设计背景
- `infographic_slide_set` (pptx_or_markdown): 包含流程、对比和指标卡的答辩版式结果

## Research Gates

- Skill identity status: `ready`
- Cocoloop slug check complete: yes
- ClawHub slug check complete: yes
- Slug available: yes
- Target environment status: `ready`
- Current environment: codex authoring workspace on macOS
- Target environment: codex authoring workspace on macOS
- Current environment is target: yes
- Implementation approach status: `ready`
- Selected execution plane: `Skill + CLI`

## Output Profile

- Has visual output: yes
- Visual output types: `ppt`

## Interaction Rules

- Plan the question budget before asking anything.
- The full interaction should normally stay within 10 total questions, including confirmation questions.
- Ask only one key question per turn and use defaults, existing context, environment detection, or confirmations to reduce follow-up questions.
- Detect the current environment early and use that result to narrow the platform and runtime discussion.
- Confirm the target runtime environment before writing any skill content, scaffold, implementation path, or build instructions.
- If the current environment might be the target environment, ask the user to confirm that explicitly after environment detection.
- If the target environment is still unclear, stop at clarification and do not start drafting the skill body or execution steps.
- If the task is already clear, skip redundant questions and move to execution or summary.
- If open gaps remain near the question limit, apply `write_open_gaps_then_continue` instead of extending the interview.

## Design Input
- For webpage, infographic, PPT, and other visual output tasks, read `references/design.md` before high-fidelity design.
- Users can keep the default official preset, switch to another preset in `references/design-md/`, or replace it with their own `DESIGN.md`.
- Current source mode: `preset`
- Current preset: `apple`
## Visual Storytelling

- Artifact family: `visual_narrative_artifact`
- Output adapters: `ppt`
- Story units: `cover`, `agenda`, `problem`, `contribution`, `method`, `experiment`, `result`, `analysis`, `closing`
- Text hierarchy: `kicker`, `headline`, `summary`, `body`, `metric`, `annotation`
- Infographic required: yes

## Must Have

- 答辩大纲建议
- 页级内容结构
- 默认 DESIGN.md 预设
- 示例 slides 结果
- 明确的文字层级
- 方法流程图、结果对比图和指标卡

## Excluded

- 不负责自动搜集论文原始数据

## Target Platforms

- `codex` (supported_public): 测试渲染平台
- `claude_code` (supported_public): 兼容渲染平台

## Dependencies

- `slides` (reference): 如环境允许，可进一步导出可编辑演示稿

## Fallback Policy

- Allowed: yes
- Summary: 缺少可编辑 PPT 依赖时，先交付结构化 slides 结果
