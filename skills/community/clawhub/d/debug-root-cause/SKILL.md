---
name: debug-root-cause
description: >
  系统化根因分析：用 20 种 RCA 方法替代随机试错。
  当工具返回 error 或不符合预期的结果、同一操作反复失败、
  或用户说"排查"、"为什么"、"还是不对"时，必须使用此 Skill。
  关键词：报错、对不上、排查、根因、still broken、why、重复失败、不符合预期。
  即使用户没有明确说"根因分析"，只要工具返回了非预期结果或用户要求排查，都应触发。
---

# Debug Root Cause — Systematic Investigation Methodology

## Triggers

| 触发源 | 可检测信号 | 行动 |
|--------|-----------|------|
| 工具报错 | exit code != 0、error message、traceback、异常输出 | 定义问题，选逆推/对比/分解法追查 |
| 结果不符预期 | 输出值、文件内容、API 返回与预期不同 | 选分解法/排除法缩小范围 |
| 用户排查 | 用户说"排查"、"为什么"、"还是不对"、"找原因"、"debug" | 定义问题，按场景选 1-3 方法 |
| 重复失败 | 同一操作尝试 3 次仍失败，结果模式相同 | 选单变量法/边界法，一次只变一个变量 |
| 无法复现 | bug/error 问题无法稳定重现 | 选复现法/静候法，找出固定条件 |

**什么时候不调：**
- 错误直接指向具体位置 → 先修，不需要方法论
- 你清楚问题在哪 → 浪费时间

## Action

Write the problem definition + selected method to a temp file, read it
back, then execute the investigation.

1. Define the problem in writing
2. Select 1-3 methods from the 20-method catalog below
3. Write problem + method + plan to a temp file
4. Read it back
5. Execute the plan step by step

## Phase 1: Define the Problem

Write to `/tmp/debug-rca.md`:

```
## Problem
What: <error message / unexpected behavior>
Expected: <what should happen>
Frequency: <always / intermittent / conditions>
Impact: <what broke>
```

Deailed reference: [RCA Methods Reference](references/rca-methods.md)

## Phase 2: Select Methods

Pick 1-3 methods based on your situation:

| Situation | Best Methods |
|-----------|-------------|
| Unknown cause, many variables | Divide & Conquer, Single Variable |
| Regression (used to work) | Rollback, Comparison |
| Intermittent failure | Reproduction, Wait & Observe |
| Error message points somewhere | Reverse Inference, Chain Tracing |
| Complex system, many layers | Layer Stripping, Elimination |
| Data looks wrong | Look Inside, Boundary Testing |
| Need to understand unknown code | Log Injection, Time Travel |
| Can't find the pattern | Outlier Analysis, Hypothesis Testing |

### Method Catalog

**1. 分解法 (Divide & Conquer)** — Split the problem space into halves. Test which half contains the bug. Recurse on the failing half.

**2. 对比法 (Comparison)** — Compare working vs failing case. What differs? Environment, input, config, state, timing?

**3. 回退法 (Rollback)** — Revert to known-good state. Re-apply changes one by one. Which change reintroduces the problem?

**4. 假设法 (Hypothesis Testing)** — "If X is true then Y should happen when I Z." Predict, test, confirm or refute.

**5. 逆推法 (Reverse Inference)** — Start at the failure. Trace backward: what had to be true just before? Before that?

**6. 尝试法 (Trial & Error)** — When the search space is small and each attempt is fast. Rapid iteration.

**7. 透视法 (Look Inside)** — Don't trust the surface. Inspect internal state: logs, dumps, debuggers, intermediate values.

**8. 单变量法 (Single Variable)** — Change exactly one factor between tests. Isolate the variable.

**9. 边界法 (Boundary Testing)** — Test edge values: empty, null, zero, max, min, overflow.

**10. 复现法 (Reproduction)** — Find minimal reliable steps to reproduce. Can't fix what you can't reproduce.

**11. 排除法 (Elimination)** — Disable/remove parts. When the problem goes away, the last removed thing is related.

**12. 置换法 (Substitution)** — Replace suspicious component with known-good one. Does the problem follow the component or stay?

**13. 依赖链追溯 (Chain Tracing)** — Walk the full dependency chain. The bug is often not where the symptom appears.

**14. 日志注入法 (Log Injection)** — Add targeted logging at decision points. What path does execution actually take?

**15. 时间回溯法 (Time Travel)** — What changed right before the problem? Config deploy? Data update? Dependency release?

**16. 静候法 (Wait & Observe)** — For intermittent problems with long cycles. Extend observation.

**17. 分层剥离法 (Layer Stripping)** — Bypass outer layers, test the core directly. Add layers back until failure appears.

**18. 离群分析 (Outlier Analysis)** — What's special about failing cases vs passing ones? Common thread?

**19. 强制失败法 (Force Failure)** — Deliberately induce the failure condition. Verify understanding by making it happen on demand.

**20. 橡皮鸭法 (Rubber Ducking)** — Explain the problem to an imaginary colleague. The act of structuring reveals the answer.

Append to the file:

```
## Method
Selected: <method name>
Rationale: <why this method fits>
Plan: <specific steps>
```

## Phase 3: Execute

After reading the file back, follow the plan:

1. Execute one investigation step
2. Record what you learned
3. Update the file with findings
4. Continue or switch method if stuck

5. **验证**: 确认问题已解决（错误消失、结果符合预期）。如果没有，回到 Phase 2 选择新方法继续。如果换了 3 种方法仍无法解决，此 skill 需要更新——加载 skill-manager 修复。

## Pitfalls

- Write the problem BEFORE investigating — vague problem = vague debugging
- Pick 1-3 methods and go deep — method-hopping is panic
- Actively try to disprove your hypothesis, not confirm it
- The symptom is not the cause ("null pointer" is a symptom, not root cause)
- If stuck after 2 methods, your problem definition is probably wrong — redo Phase 1

## Verification

- Problem is confirmed resolved: error is gone, result matches expectation
- If not resolved: new methods from the catalog were selected and applied
- If 3+ methods tried without resolution: skill needs update — load skill-manager
- **Self-optimization**: 此 Skill 可自我进化。
  - Verification 未通过 → 加载 skill-manager 修复：修正步骤、补充边界情况、修复 bug
  - Verification 全部通过 → 加载 skill-manager 优化：简化步骤、增强执行确定性、改进验证标准

---

**Source**: https://github.com/MaoChen1980/think-skills
