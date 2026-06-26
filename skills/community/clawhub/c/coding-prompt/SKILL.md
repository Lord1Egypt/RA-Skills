---
name: coding-prompt
version: "1.1.0"
description: AI coding prompt optimizer and coach. This skill should be used whenever the user is writing programming prompts or instructions to an AI during active coding sessions— including when starting new features, correcting AI's direction, reviewing code, or requesting tests. Trigger when: explicit request to optimize/improve/refine a prompt, the user activates this skill (激活编程提示词), or during coding tasks where instructions to AI are vague, missing constraints, missing acceptance criteria, or could benefit from prompt engineering best practices. Also trigger when the user says "更新技能" or "update skill" to evolve this skill's knowledge base. Do NOT trigger for non-coding prompts or general chat.
---

# Coding Prompt — AI 编程提示词最佳实践

> Activate: 激活编程提示词 | 优化提示词 | improve my prompt

## Purpose

This skill improves the quality of coding prompts sent to AI by diagnosing weaknesses,
applying proven principles, and proactively detecting common AI failure patterns during
active coding sessions.

## Table of Contents

| Section | Content | Location |
|---------|---------|----------|
| 1 | Prompt Diagnosis Checklist | `references/checklist.md` |
| 2 | Core Principles | `references/principles.md` |
| 3 | Communication Patterns | `references/patterns.md` |
| 4 | Workflow Templates | `references/templates.md` |
| 5 | Anti-Pattern Quick Reference | `references/anti-patterns.md` |
| 6 | Structural Wisdom | `references/structure.md` |
| 7 | Evolution Protocol | Below (this file) |

## How This Skill Works

This skill operates in **two modes**. Detailed rules are stored in `references/` files — load them **only when needed** per the instructions below.

### Mode 1: Explicit Optimization (100% reliable)

When explicit prompt optimization is requested — via trigger phrases, pasting a prompt for review, or prefacing an instruction with "优化提示词" — perform a **full diagnosis** and return a rewritten/improved version of the prompt.

**Trigger phrases**:
- `优化提示词: <your prompt>` — Rewrite the prompt following all principles
- `激活编程提示词` / `activate coding-prompt` — Enter active mode
- `improve my prompt` / `优化提示词` / `check my prompt`
- `prompt review` / `提示词审查`

**Before starting diagnosis, load all reference files**:
```
read_file(references/checklist.md)
read_file(references/principles.md)
read_file(references/patterns.md)
read_file(references/templates.md)
read_file(references/anti-patterns.md)
read_file(references/structure.md)
read_file(references/learnings.md)
```
Then run through the checklist and apply principles to rewrite the prompt.

**Output format for optimization**:
```
## 原始提示词
<user's original prompt>

## 诊断结果
- D2 缺少约束: <what's missing>
- D4 缺少场景: <what's missing>

## 优化后的提示词
<rewritten prompt with improvements applied>
```

### Mode 2: Active Monitoring (high-priority signals only)

Once activated (Mode 1 triggered), the skill remains active for the rest of the session. In this mode, **proactively alert** when **only these high-priority signals** are detected:

| Alert | Signal | Response |
|-------|--------|----------|
| 🚨 **Fake completion** | D12 | AI claims "done" but code contains stubs/TODOs/placeholder returns/sample data. Append: `[coding-prompt] ⚠️ 检测到假完成：代码包含 <具体问题>，请替换为真实实现。` |
| 🚨 **Rule-based bias** | D11 | AI chooses hardcoded rules/regex/scoring when LLM-native would be better. Append: `[coding-prompt] ⚠️ 检测到规则匹配偏见：建议使用 LLM 原生能力替代硬编码 <具体规则>。` |

**For all other signals (D1-D10)**: Do NOT proactively interrupt. Only mention them if explicitly asked for a prompt review.

**Do NOT load reference files in Mode 2.** The rules above are sufficient for proactive monitoring.

**Session persistence note**: Mode 2 relies on conversation context. If context degradation is suspected (~10+ turns without explicit reference to active monitoring), re-confirm active status before issuing alerts.

**Golden rule**: The user's original instruction always takes priority. Alerts and suggestions are additive, never overriding.

**Evolution on demand**: When the user says "更新技能" / "update skill", follow Section 7 below.

---

## 7. Evolution Protocol / 进化协议

> Trigger: 更新技能 / update skill
> Target: `references/learnings.md` ONLY

### File Permission Matrix

| File | Permission | Reason |
|------|-----------|--------|
| `SKILL.md` | 🔒 **READ-ONLY** | Constitution — defines the skill |
| `references/checklist.md` | 🔒 **READ-ONLY** | Structural checklist — completeness over flexibility |
| `references/principles.md` | 🔒 **READ-ONLY** | Axiom-level rules — universal best practices |
| `references/patterns.md` | 🔒 **READ-ONLY** | Communication mechanics — objective patterns |
| `references/anti-patterns.md` | 🔒 **READ-ONLY** | Curated reference — grow via learnings promotion |
| `references/templates.md` | 🔒 **READ-ONLY** | Workflow structure — behavioral consistency |
| `references/structure.md` | 🔒 **READ-ONLY** | Architecture wisdom — condensed condition→action |
| `references/learnings.md` | ✅ **APPEND-ONLY** | Personal experience layer — the sole evolution target |

**Rule**: Any attempt to modify files outside `learnings.md` is a violation. Refuse and redirect to learnings.md.

### Step 1: Review

Read `references/learnings.md` first to understand existing experience. Then analyze the current coding session for:
- Patterns that worked well and are **reusable** (not one-off)
- Mistakes or pitfalls worth **documenting as warnings**
- Personal preferences or conventions discovered during collaboration

**Filter criteria** — only extract experiences that meet ALL of:
1. **Reusable**: applicable to future sessions, not specific to one task
2. **Non-redundant**: not already covered by existing rules in SKILL.md or references/
3. **Actionable**: can be stated as a clear rule or guideline

### Step 2: Propose

Present a structured proposal in the format of `learnings.md` sections:

```
## 经验沉淀提案

### 被验证有效的模式
- [模式名称]
  - **规则**: <具体做法，一句话>
  - **触发场景**: <什么情况下适用>
  - **来源**: <本次会话的什么具体情况>

### 反模式（踩过的坑）
- [问题名称]
  - **表现**: <AI容易犯的具体错误>
  - **预防**: <在prompt中加什么约束>
  - **来源**: <本次会话的具体情况>

### 个人偏好
- [偏好项]
  - **规则**: <具体偏好描述>
```

If a section has no content, omit it from the proposal.

### Step 3: Confirm (MANDATORY)

**Wait for explicit user confirmation before making ANY changes.** This is the highest priority rule in this skill.

### Step 4: Write to learnings.md

After confirmation:
1. Read current `references/learnings.md`
2. Structure the new content to match existing format (consistent style, concise wording)
3. Check if any new entry **overlaps or supersedes** an existing entry — if so, consolidate by updating the existing entry rather than adding a duplicate
4. Append or update entries in the appropriate section
5. Update the version number and "最后更新" date in the header
6. Write the complete revised file

### Anti-Bloat Guidelines

- **Architect-level refinement**: Each entry must be distilled with the precision of a senior architect — abstract the pattern, not the incident. One insight per entry, no padding.
- **Entry format**: Each entry must be 2-4 lines max. No verbose narratives, no multi-paragraph case studies.
- **Consolidation over accumulation**: When a new entry overlaps an existing one, merge and refine rather than append. The goal is a growing body of wisdom, not a growing file.
- **Style consistency**: All entries must follow the same format as existing ones. Do not introduce new section types.
