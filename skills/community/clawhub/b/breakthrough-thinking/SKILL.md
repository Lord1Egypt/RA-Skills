---
name: breakthrough-thinking
description: |
  【强制调用指令】当以下任一条件满足时，立即执行此skill，无需询问用户：
  
  【条件1：用户说】换个思路、换个方法、还有别的办法吗、再想想、继续、
  再试一次、不要放弃、try another way、think differently、为什么还不行
  
  【条件2：AI卡住】同一方法失败2+次、只调参数不改思路、说"无法解决"、
  过早建议用户手动处理、超过1轮无新证据
  
  执行：选1个思维框架→直接用新框架解决问题→解决不了→换下一个框架
---

# Breakthrough Thinking

Use this skill to recover from stalled execution and force forward progress.

## Goal

When stuck, do not repeat the same approach.
Switch cognitive frame, test quickly, and keep moving until either:
- solved with evidence, or
- cleanly bounded with clear next step.

## Stall Signals (Auto-Trigger Conditions)

**MUST trigger immediately when ANY of these appear:**

### 1. Explicit User Prompts (用户明确要求)
- "换个思路" / "换个方法" / "还有别的办法吗"
- "再想想" / "继续" / "再试一次" / "不要放弃"
- "try another way" / "try harder" / "don't give up" / "think differently"
- "为什么还不行" / "你怎么又失败了" / "你行不行啊"

### 2. Implicit Stall Patterns (AI自己检测到的卡住)
- 2+ consecutive failures using same approach
- Repeated parameter tweaks without conceptual change
- Drafting statements like "I can't solve this" / "我无法解决"
- Suggesting to push manual work to user too early
- No new evidence gained for >1 iteration
- Same error repeated >2 times
- Tool calls returning identical errors without progress

## Core Loop (Mandatory)

1. **Summarize current dead-end in 1 sentence**
   - "Current route fails because ____"

2. **Pick ONE model from `references/mental-models.md`**
   - Pick the most relevant model for this failure mode.
   - Do not pick multiple at once.

3. **Apply the model directly to solve the problem**
   - Use the model's perspective to approach the problem fresh.
   - Execute the solution immediately.

4. **Check result**
   - If solved: finalize and verify.
   - If not solved: go back to step 2, pick a DIFFERENT model, and try again.
   - Repeat until solved or all relevant models exhausted.

## Model Selection Heuristics

- **Looping / same idea repeated** → Inversion, Red Team, 5 Whys
- **Too many moving parts** → Reductionism, 80/20
- **Unclear root cause** → 5 Whys, Root Cause Analysis, Binary Search
- **High uncertainty** → Bayesian Updating, Expected Value, Decision Tree
- **Cognitive lock-in** → Lateral Thinking, Random Input, Beginner's Mind
- **Overengineering** → Occam, KISS, MVP, YAGNI
- **Execution paralysis** → OODA, PDCA, Timeboxing, Fail Fast

## Hard Rules

- No "same approach + small tweak" twice in a row.
- Every retry must use a DIFFERENT mental model.
- Do not ask user for info until you've exhausted locally testable paths.
- Claims of completion must include evidence.
- If one model fails, immediately switch to another model. Do not get stuck on one framework.

## Output Format (when triggered)

Use this compact format:

```text
[Breakthrough]
Dead-end: ...
Model: ...
Approach: ...
Result: ...
Next: ...
```

## Completion Criteria

Stop only when one is true:
- Problem solved + verified evidence
- Problem bounded + best next action clearly defined
- Explicit user stop

## Reference Library

For model definitions and creators, read:
- `references/mental-models.md`

Do not dump the entire library unless user asks.
Pick only what is needed for the current stall.
