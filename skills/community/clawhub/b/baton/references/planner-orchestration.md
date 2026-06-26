# Planner-Orchestrator protocol

Goal: convert any user request into the smallest safe delegated execution graph. The planner is always the first child.

## Planning algorithm

1. **Objective:** restate the user outcome in one sentence.
2. **Risk:** low, medium, or high. High includes destructive, external, production, credentials, payment, medical/legal/financial, security, compliance, or brand-risk work.
3. **Mode:** inherit user/main config; otherwise standard. Use quick for trivial, careful/high-confidence for high-risk, creative for campaigns/content, private when external tools should be avoided, rate-safe when provider capacity is constrained.
4. **Shape:** choose `micro`, `single_worker`, or `dag`.
5. **Roles:** pick by outcome/channel. Collapse roles unless separation clearly improves quality, safety, or context use.
6. **Models:** map each task to a tier, not a hard-coded model. Parent/router resolves actual allowed model.
7. **Context:** isolated by default; fork only if transcript state is required.
8. **Validation:** add gates only when risk/quality warrants them.
9. **Rate:** serialize, parallelise, spread providers, or collapse roles.
10. **Output:** specify the exact final answer shape.

## Shape rules

- `micro`: one planner result or one tiny worker; use for definitions, simple rewrites, short answers, small calculations, quick advice.
- `single_worker`: one specialist can produce the answer; use for ordinary research, drafting, support, ops, content, or code inspection.
- `dag`: use for multi-source research, campaigns, code/config changes, long docs, agentic operations, high-risk work, conflicting evidence, or any task needing independent validation.

## Spawnable DAG schema

```json
{
  "planType":"dag",
  "summary":"one sentence",
  "mode":"standard",
  "risk":"medium",
  "tasks":[
    {"taskId":"research_audience","role":"market_researcher","goal":"identify audience and constraints","dependsOn":[],"tier":"balanced","contextMode":"isolated","budget":"s","acceptanceCriteria":["3 actionable insights"]},
    {"taskId":"draft_assets","role":"social_media_manager","goal":"draft channel-specific assets","dependsOn":["research_audience"],"tier":"creative","contextMode":"isolated","budget":"m","acceptanceCriteria":["platform-specific","brand voice"]},
    {"taskId":"brand_check","role":"brand_safety_reviewer","goal":"review for brand/compliance risk","dependsOn":["draft_assets"],"tier":"balanced","contextMode":"isolated","budget":"s","acceptanceCriteria":["clear pass/fail"]}
  ],
  "validationGates":["brand_check required before posting"],
  "rateLimitStrategy":"spread_providers",
  "finalOutputShape":"brief strategy + final assets + risks"
}
```

## Efficiency rules

- Default budget: planner `s`, workers `s`, validator `s`; use `m/l` only for long context or high stakes.
- Maximum default workers: quick 1, standard 2, careful/high-confidence 3, rate-safe 1 serial.
- Prefer one combined worker for adjacent roles: researcher+analyst, writer+editor, social+community, ops+admin.
- Never include long background, chain-of-thought, or full transcripts in child prompts.

## Parent handling

If planner completes the result, parent checks gates and answers. If planner returns a DAG and nested spawning is unavailable, parent spawns ready leaf tasks in dependency order. Leaf workers must not spawn children.
