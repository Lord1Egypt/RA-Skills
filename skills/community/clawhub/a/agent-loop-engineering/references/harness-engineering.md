# Harness Engineering

Use this reference when the task needs a longer-running AI coding harness instead of a single-agent coding loop. A harness is the control system around agents: context control, role separation, evaluation feedback, workflow orchestration, environment observability, and stop rules.

## 中文快速说明

Harness Engineering 是围绕 Agent 构建的工程化运行环境。它不等于单个 Coding Agent，而是把目标、上下文、执行、评估、反馈、环境可读性和停止规则组合成一个可观察、可控制、可迭代的系统。

核心原则：

- 越简单越好，默认只保留规划、执行、验证三个必要环节。
- 目标要求必须传递给每个 Agent；实现思路不应传递给独立评估 Agent。
- 写代码的 Agent 和评估质量的 Agent 应分离，避免自我评分偏正向。
- 每个 Agent 只读取完成自己职责所需的上下文。
- 自动化循环必须有目标分数、最大轮次、连续失败上限和边际收益停止条件。
- UI、日志、测试数据、浏览器截图、DOM、API 响应和运行日志应尽量暴露给 Agent，形成可验证环境。

## Minimal Harness Shape

Prefer this shape before adding more roles:

```text
Planner -> Developer -> Evaluator -> Continue / Replan / Done / Blocked
```

Responsibilities:

| Role | Reads | Writes | Must Not Do |
| --- | --- | --- | --- |
| Planner | User goal, constraints, product context | `TARGET.md`, `ACCEPTANCE.md`, task plan, quality vision | Implement code before target is clear |
| Developer | Target, task contract, relevant code, verification commands | Code changes, self-test evidence, implementation notes | Judge final quality alone |
| Evaluator | Target, acceptance criteria, rubric, running app evidence | Evaluation report, pass/fail evidence, repair requests | Read developer reasoning unless needed for debugging |

The main agent or runner coordinates files and state transitions. It should not become the only evaluator.

## Context Separation

Use context separation to reduce bias and token cost:

- Planner receives product goals and user constraints.
- Developer receives the task contract, relevant code, and verification requirements.
- Evaluator receives acceptance criteria, rubric, app evidence, and observable behavior.
- Evaluator should not receive the developer's intended implementation path by default.
- Full chat history should not be passed across roles; pass structured files instead.

If a role needs more context, it must request a specific file or evidence item, not the entire history.

## Required Artifacts

For harness-style work, add these files under `Docs/` when useful:

- `Docs/QUALITY_VISION.md`: quality level, positive/negative references, UI/UX anchors, style constraints, density, interaction expectations.
- `Docs/RUBRIC.md`: weighted evaluation checklist.
- `Docs/TEST_CASES.md`: functional and edge-case test cases.
- `Docs/E2E_CASES.md`: browser or end-to-end flows with evidence requirements.
- `Docs/EVALUATION.md`: score, pass/fail evidence, repair suggestions, stop decision.

Do not create these files for small bug fixes unless the acceptance surface is ambiguous or subjective.

## Quality Vision

Use `Docs/QUALITY_VISION.md` when the user asks for UI, UX, product polish, creative experience, or production-level quality.

Recommended fields:

```markdown
# Quality Vision

## Quality Level
MVP / Polished / Production-grade

## Positive Anchors
- URL or screenshot:
- What is good:
- Which parts apply:

## Negative Anchors
- URL or screenshot:
- What to avoid:

## Visual Direction
- Layout:
- Color:
- Density:
- Motion:
- Component style:

## Interaction Expectations
- Primary flow:
- Feedback states:
- Loading states:
- Error states:
- Mobile/desktop expectations:

## Quality Red Lines
- Must not:
```

Quality vision prevents "the feature works but looks unfinished" failures.

## Rubric Evaluation

Use rubric evaluation when quality is subjective, broad, or repeatedly under-specified.

Rubric principles:

- Grounded in expert guidance: reflect the user's domain, architecture, product, security, or UX standards.
- Comprehensive coverage: include correctness, completeness, robustness, style, safety, and common pitfalls.
- Weighted importance: separate Essential, Important, Optional, and Pitfall criteria.
- Self-contained: each criterion must be judgeable without hidden context.

Suggested weights for frontend product work:

| Layer | Weight | Focus |
| --- | ---: | --- |
| L1 Functional correctness | 0.40 | Business logic, data changes, state flow, API integration |
| L2 Robustness | 0.25 | Edge input, errors, concurrency, race conditions, security pitfalls |
| L3 UI presentation | 0.20 | Rendering, layout, responsive behavior, visual consistency |
| L4 Interaction experience | 0.15 | Feedback, loading, affordance, keyboard/accessibility, flow quality |

Example rubric item:

```markdown
- id: L1-USER-FILTER
  type: Essential
  weight: 1.0
  criterion: Search filtering shows only matching users and does not keep stale full-list rows.
  evidence: Browser operation plus DOM assertion, or state/API evidence.
```

Pitfall items should describe serious failure modes such as data loss, XSS, duplicate submissions, blank screens, layout overlap, or silent API failure.

## Evaluation Loop

Use this loop when the user explicitly wants autonomous improvement or when the quality target requires multiple feedback rounds:

```text
Developer implements task
Evaluator runs rubric and observable checks
If score below threshold and budget remains:
  Developer fixes from evaluator report
  Evaluator re-runs changed cases
If repeated score gain is low:
  stop as Done with Risk or ask user whether to continue
```

Recommended defaults:

```yaml
min_required_score: 0.90
target_score: 0.95
min_feedback_loops: 1
max_feedback_loops: 5
max_consecutive_low_gain_loops: 2
low_gain_delta: 0.03
```

Do not force long loops for simple deterministic tasks. Long loops are useful only when new evidence can change the result.

## Environment Readability

Agent quality improves when the application is observable and operable. Prefer evidence the agent can inspect directly:

- Test commands, type checks, builds, and linters.
- Browser automation with screenshots, DOM snapshots, console logs, and network traces.
- API responses, local fixtures, mock data, and test accounts prepared before the loop.
- Runtime logs, error logs, trace IDs, metrics, and local observability outputs.
- Screenshot comparison or visual inspection when UI quality is part of acceptance.

If the environment requires login, secrets, production data, paid resources, system installs, or irreversible operations, stop under the hard stop rules.

## Stop on Low Marginal Gain

Long-running loops can waste time by improving tiny details after the core target is met. Stop or ask the user when:

- Score improvement is below `low_gain_delta` for `max_consecutive_low_gain_loops`.
- Remaining failures are Optional only.
- Fixes are mostly cosmetic and not covered by the user's quality level.
- Further progress requires new human taste input or external references.
- The same evaluator complaint repeats without objective improvement.

Use `Done with Risk` when the core goal is complete but quality polish remains below the desired level.

## When Not to Use Full Harness

Avoid full multi-agent harness orchestration when:

- The task is a narrow bug fix with clear reproduction and tests.
- The acceptance criteria are deterministic and already covered by tests.
- The project does not have a runnable or inspectable environment.
- The overhead of Planner/Developer/Evaluator separation exceeds the risk.
- The user asked for a quick local change, not long-running autonomous work.

In those cases, use the normal Agent Loop Engineering one-loop flow.
