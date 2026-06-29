# AI Coding Production System

Use this reference when designing or auditing a long-running, high-risk, multi-agent, or quality-critical AI coding workflow. It compresses production and food-safety management systems into practical Agent Loop Engineering controls.

Do not load this file for ordinary bug fixes. Use it when the work needs stronger control than a normal one-loop coding task.

## 中文快速说明

AI Coding Production System 的目标不是把 TPS、TQC、Six Sigma、ISO、HACCP、FSSC 22000 等管理体系变成管理学资料库，而是抽取它们最适合约束 AI Agent 的控制机制。

核心判断：

- 稳定、高质量、可复制的产出，不靠 Agent 自觉。
- 需要标准作业、质量内建、异常停止、关键控制点、独立审核、追溯记录和持续改善。
- Agent 可以自由写代码，但不能自由宣布完成。
- 规则要尽量落到 `Docs/` 模板、checker、runner 或 MCP tool，而不是只停留在说明文字。

## Source Systems

| Source system | Useful mechanism | Agent Loop meaning |
| --- | --- | --- |
| TPS | Jidoka, Just-in-Time, Kaizen, Gemba, waste reduction | Stop on abnormal state, use minimal increments, inspect real evidence, reduce wasteful loops |
| TQC / TQM | Customer orientation, total participation, built-in quality | Planner, Developer, Evaluator, Runner all own quality |
| Six Sigma | DMAIC, data-driven variation reduction, control | Systematic debugging and quality metrics |
| ISO 9001 | Process approach, risk-based thinking, documented information | Make the loop auditable and repeatable |
| ISO 22000 | PRP, HACCP, PDCA, traceability, management system | Preconditions, risk analysis, control points, records |
| FSSC 22000 | Scheme requirements, certification, integrity monitoring | Independent audit and system integrity checks |
| HACCP / Codex | Hazard analysis, CCP, monitoring, corrective action, verification, records | Identify failure modes and enforce critical gates |
| FSMA preventive controls | Risk-based preventive controls | Prevent likely failure instead of only reacting after failure |
| GFSI | Benchmarking, harmonization, capability building | Shared standards across different agents and runners |
| 8D / Five Whys | Root cause and corrective action | Avoid repeated shallow fixes |

## Ten Control Rules

These are the only production-system rules that should become core controls.

| Rule | Production source | Agent Loop control |
| --- | --- | --- |
| Direction Alignment | Hoshin Kanri, ISO 9001 | Keep `DIRECTION.md -> TARGET.md -> ACCEPTANCE.md` aligned |
| Standard Work | TPS, TQC | Every loop follows the same minimum execution contract |
| Built-in Quality | Jidoka, TQC | Verification is part of every loop, not a final afterthought |
| Just-in-Time Context | TPS JIT | Read only the context needed for the current control point |
| Hazard Analysis | HACCP, ISO 22000 | Identify likely failure modes before long-running work |
| Critical Control Points | HACCP, FSMA | Define gates that block Continue or Done when failed |
| Data-Driven Verification | Six Sigma, ISO | Use tests, logs, metrics, screenshots, DOM, API evidence |
| Root Cause Corrective Action | DMAIC, 8D, Five Whys | Repeated failure requires root cause before more changes |
| Traceability Records | ISO 22000, FSSC | Record loop, evidence, files, decision, and next action |
| Continuous Improvement | Kaizen, PDCA, ISO | Improve templates, checks, and rules from repeated failures |

## Food-Safety Control Model

Food safety systems are useful because they handle low-tolerance production with changing conditions and unexpected events.

Map the food-safety pattern to coding:

```text
PRP / prerequisites
  -> Hazard analysis
    -> Critical control points
      -> Monitoring
        -> Correction / corrective action
          -> Verification
            -> Records
              -> Audit
                -> Continuous improvement
```

Agent Loop version:

```text
Development prerequisites
  -> Agent failure mode analysis
    -> Test / build / security / acceptance gates
      -> Loop evidence
        -> Fix or root-cause corrective action
          -> Automatic and functional verification
            -> LOOP_RUNS.jsonl and EVALUATION.md
              -> Evaluator / checker / CI audit
                -> Template and skill improvement
```

## Practical Mapping to Existing Docs

Do not create many new files by default. First map controls to existing `Docs/` files.

| Production concept | Preferred Agent Loop file |
| --- | --- |
| PRP / prerequisites | `Docs/LOOP_CONFIG.md` |
| Direction alignment | `Docs/DIRECTION.md` when available, otherwise `Docs/TARGET.md` |
| Hazard analysis | `Docs/ACCEPTANCE.md` risk / failure examples section |
| Critical control points | `Docs/ACCEPTANCE.md` must-pass criteria |
| Critical limits | `Docs/ACCEPTANCE.md` evidence requirements and failure examples |
| Monitoring | `Docs/EVALUATION.md` |
| Corrective action | `Docs/PENDING.md` and `Docs/EVALUATION.md` |
| Verification | `Docs/EVALUATION.md` and `Docs/ACCEPTANCE.md` current evidence |
| Traceability | `Docs/LOOP_RUNS.jsonl` |
| Audit | checker / evaluator / CI output |
| Continuous improvement | `Docs/HANDOFF.md`, skill updates, template updates |

Create separate files such as `RISK_ANALYSIS.md`, `CONTROL_POINTS.md`, or `AUDIT.md` only when the project is large, regulated, high-risk, or multi-agent enough to justify them.

## Built-in Quality Rule

Apply this rule to long-running or quality-critical work:

```text
Every coding loop must include defined control points, monitoring evidence, corrective action for failures, and verification records.
An agent may not continue or claim Done when a critical control point is failed or unverified.
```

中文：

```text
每个 coding loop 必须包含控制点、监控证据、失败纠正和验证记录。
关键控制点失败或未验证时，Agent 不允许继续假装完成，也不允许声明 Done。
```

## Control Point Examples

| Control point | Failed when | Required action |
| --- | --- | --- |
| Target alignment | Current action does not serve `TARGET.md` | Stop as `Blocked` or revise target with human approval |
| Test gate | Required tests fail | Diagnose, fix, re-run, or record blocker |
| Type/build gate | Typecheck or build fails | Fix before Done |
| Functional gate | Feature cannot be demonstrated | Continue or Done with Risk if explicitly limited |
| Security gate | Secret, production data, or destructive action is needed | Stop as `Blocked` |
| UI quality gate | Rubric or quality vision fails | Continue if budget remains; otherwise Done with Risk |
| Traceability gate | Loop evidence cannot be reconstructed | Invalid state; repair state before continuing |

## Metrics

Use lightweight metrics only. Metrics should help stop wasteful loops, not create reporting work.

Suggested metrics:

- Loop count.
- Consecutive failures.
- Verification pass/fail.
- Root cause category.
- Rework count.
- Low-gain loop count.
- Time spent blocked.
- Evidence completeness.

Avoid vanity metrics such as lines of code changed, number of files touched, or token volume without quality evidence.

## When to Use This Reference

Use this reference when:

- The task is long-running, multi-stage, or high-risk.
- Multiple agents or runners are involved.
- The user wants production-grade, auditable, or highly reliable output.
- There is a history of false Done, repeated failures, or target drift.
- You are designing templates, checkers, runners, MCP tools, or quality gates.

Do not use it when:

- The task is a small, deterministic bug fix.
- Acceptance criteria are already obvious and tests cover the behavior.
- Loading the reference would add more overhead than control value.

## Implementation Priority

Implement production-system controls in this order:

1. Templates for `TARGET.md`, `ACCEPTANCE.md`, `EVALUATION.md`, `LOOP_CONFIG.md`, and `NEXT_ACTIONS.md`.
2. Checker that validates state, evidence, stop rules, and Done claims.
3. Runner that continues only when the checker returns `Continue`.
4. MCP tools only after the checker behavior is stable.

The production-system idea should harden the loop, not make the Skill larger every time a new management method is discovered.
