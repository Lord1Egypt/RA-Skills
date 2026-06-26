# AgentOS / Multi-Agent Review Rubric

Use this reference only when reviewing AgentOS, multi-agent systems, LLM orchestration kernels, model-routing layers, workflow engines, or autonomous agent platforms.

## Scoring Scale

0 = absent or harmful  
1 = exists as a manual process  
2 = partially automated but easy to bypass  
3 = closed loop with basic damping/gates  
4 = adaptive loop using historical outcomes  
5 = self-improving loop with guardrails against drift and pollution

## Dimensions

| Dimension | What score 5 looks like |
|---|---|
| Default entrypoint unity | All normal scheduling/execution/tool paths pass through one kernel or orchestrator. |
| Model routing adaptiveness | Routing uses task complexity, budget, health, latency, historical success/failure, and preference. |
| Token damping | High-volume outputs are command-aware compressed; saved ratio and loss risk are observable. |
| Workflow gate strength | Workflow steps require evidence; failures loop back to the correct step. |
| Memory pollution resistance | Runtime observations, failures, SOP candidates, and long-term knowledge are separated and promoted through gates. |
| Feedback-to-policy loop | Cost, failure, latency, and review outcomes tune future routing, budgets, or workflow choices. |
| Explainability | Decisions have request ids, factors, scores, fallback chains, and human-readable reasons. |
| Safety boundary | Irreversible, public, destructive, or over-budget actions pause for confirmation. |

## Common Deductions

- Any direct execution path bypassing the kernel: -1 to -2 on entrypoint unity.
- Logs recorded but never used in future decisions: cap feedback-to-policy at 2.
- Long-term memory writes without filtering or promotion: cap memory pollution resistance at 2.
- Compression without original/compressed/saved metrics: cap token damping at 3.
- Workflow steps without required artifacts: cap workflow gate strength at 2.
- No human confirmation for risky actions: cap safety boundary at 2.
