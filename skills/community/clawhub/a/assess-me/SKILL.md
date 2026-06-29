---
name: assess-me
description: >
  认知状态审计：检查当前推理是否存在不确定性、矛盾或盲点。
  当用户质疑（"你确定吗"、"再检查"、"review"）、工具结果异常或为空、
  或修复后需验证完整性时，必须使用此 Skill。
  关键词：你确定吗、再检查、review、verify、审计、double check、检查完整性。
  即使用户没有明确说"审计"，只要用户质疑你的判断或工具返回意外结果，都应触发。
---

# Assess Me — Self-Cognition Audit

## Triggers

| 触发源 | 可检测信号 | 行动 |
|--------|-----------|------|
| 用户质疑 | 用户说"你确定吗"、"再检查"、"review"、"verify"、"确认一下" | 执行 6 问审计，摊开假设和证据 |
| 工具异常 | `read_file`/`grep`/`exec` 返回空值、报错、或明显不合理的结果 | 列出所有解读，追溯矛盾源 |
| 修复后验证 | 刚执行完修复步骤，需要确认完整性 | 检查修复是否覆盖根因，而非表面 |
| 需求模糊 | 用户指令可解读为多种互斥方式 | 列出所有解读，确认用户意图后再执行 |
| 未验证假设 | 推理链中依赖了未确认的前提条件 | 显式列出所有假设，逐个确认 |

**没有以上信号不调。** assess-me 是认知审计，不是常规工具。

## Action

Write your current thinking state to a temp file, then read it back.

1. Answer 6 questions and write to a temp file
2. Read it back
3. Critically analyze what you wrote
4. Continue based on the findings

5. **验证**: 此 skill 没有独立的 Verification 章节。检查第 3 步的分析是否全面、是否有遗漏的盲点。如果有，补充分析。

## Questions

1. **Goal** — What is the task? What does "done" look like?
2. **Progress** — What's done? What's pending?
3. **Gaps** — What information do you need but don't have?
4. **Assumptions** — What unverified beliefs are driving your approach?
5. **Blocker** — What specifically is blocking you? (exact obstacle, not symptom)
6. **Recovery** — If stuck, what should you do differently?

## Instructions

```
Write tool → /tmp/assess-me.md
Content:
# Assess Me

**Goal:** <1-2 sentences>
**Progress:** <1-2 sentences>
**Gaps:** <1-2 sentences>
**Assumptions:** <1-2 sentences>
**Blocker:** <1-2 sentences>
**Recovery:** <1-2 sentences>
```

After writing, use Read tool to read `/tmp/assess-me.md` back. Then review critically:

- Is "progress" just restating effort without results?
- Are blockers specific or vague?
- Is "Recovery" a concrete action, or just "keep trying"?
- Are you assuming something without evidence?

## Pitfalls

- Assumptions section must NOT be empty — there are always assumptions
- Recovery ≠ "keep trying" — name a specific next action
- Vague blocker = you haven't found it yet
- Read the file back — writing without re-reading skips the detachment effect

## Output Convention

When done, summarize findings inline:

```
[assess]
Goal: ...
Blocker: ...
Next: ...
[/assess]
```

## Verification

- The critical review covers all 6 questions: Goal, Progress, Gaps, Assumptions, Blocker, Recovery
- "Progress" identifies results, not just effort
- Blockers are specific, not vague
- "Recovery" names a concrete next action, not "keep trying"
- Assumptions are surfaced and examined
- Any blind spots found were supplemented with analysis
- **Self-optimization**: 此 Skill 可自我进化。
  - Verification 未通过 → 加载 skill-manager 修复：修正步骤、补充边界情况、修复 bug
  - Verification 全部通过 → 加载 skill-manager 优化：简化步骤、增强执行确定性、改进验证标准

---

**Source**: https://github.com/MaoChen1980/think-skills
