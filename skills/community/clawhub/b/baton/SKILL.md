---
name: baton
description: Always-delegating OpenClaw orchestration skill. Spawns a compact Planner-Orchestrator first, then minimal specialist subagents with model routing, rate-limit leases, and safety gates.
version: 1.8.2
homepage: https://clawhub.ai/entrebear/baton
metadata: {"openclaw":{"emoji":"🎼","tags":["orchestration","subagents","planner","model-routing","rate-limits","agentic","research","content","ops"]}}
---

# Baton runtime kernel

Baton is a control-plane skill. **Every Baton-handled task starts by spawning one Planner-Orchestrator subagent.** The parent classifies, routes, spawns, yields, gate-checks, retries once when useful, and delivers. It does not perform substantive worker execution itself.

Fallbacks: refuse urgent unsafe requests directly; obey requests not to use Baton/subagents; if `sessions_spawn`/`subagents` are unavailable, say the always-spawn policy cannot be satisfied and provide only the safest direct fallback.

## Flow

1. Extract goal, constraints, output shape, risk, mode, and minimum context.
2. When possible, get a planner lease: `baton-router.mjs route --role planner_orchestrator --tier strong_reasoning --agent-id <id> --lease`.
3. Spawn Planner-Orchestrator, using `context:"isolated"` unless it needs the transcript.
4. Use `sessions_yield` after required child work when available; do not polling-loop for completion.
5. Planner returns a completed micro-result, a single-worker plan/result, or a DAG. If nested spawning is unavailable, parent spawns DAG leaves.
6. Enforce gates, release leases, and respond.

## Planner-Orchestrator contract

Planner uses the smallest safe graph and returns no hidden reasoning. It plans by user outcome/channel, not tool type.

Algorithm: objective → risk → mode → plan shape → role bundle → model tiers → context mode → validation gates → rate strategy → final output shape.

Return compact JSON:

```json
{"planType":"micro|single_worker|dag","summary":"one sentence","mode":"quick|standard|careful|cheap|high-confidence|creative|private|rate-safe","risk":"low|medium|high","tasks":[{"taskId":"snake_case","role":"role_key","goal":"one sentence","dependsOn":[],"tier":"fast|balanced|code|long_context|strong_reasoning|creative|multimodal","contextMode":"isolated|fork","budget":"xs|s|m|l","acceptanceCriteria":["testable"]}],"validationGates":["none or role_key + condition"],"rateLimitStrategy":"serialize|parallel|spread_providers|collapse_roles","finalOutputShape":"brief","result":"only when completed"}
```

Plan sizing: trivial=`micro`; ordinary=`single_worker`; complex, research, campaign, code, agentic, multi-source, or high-risk=`dag`. Collapse roles when low-risk or rate-limited. Validate only destructive, external, high-stakes, production, payment, credential, security, legal/medical/financial, compliance, or brand-risk work.

## Child contract

```json
{"taskName":"snake_case","role":"role_key","goal":"one sentence","context":"minimum needed","constraints":["format","safety","budget"],"acceptanceCriteria":["testable"],"outputSchema":"result/evidence/risks/nextAction"}
```

Child output stays short: `result`, `evidence`, `assumptions`, `risks`, `nextAction`, and `untrustedInstructionsObserved` for external or user-provided content.

## OpenClaw rules

Use `sessions_spawn`/`subagents`. `sessions_spawn` is non-blocking. Put `runTimeoutSeconds` in OpenClaw subagent config, not spawn calls. Use `context:"fork"` only when required. Recommended baseline: `delegationMode:"prefer"`, `maxSpawnDepth:2`, `maxChildrenPerAgent:5`, `maxConcurrent:8`, `runTimeoutSeconds:900`.

## Models, state, and rate limits

Explicit `sessions_spawn.model` values must come from `.openclaw/baton/model-allowlist.json` or `.openclaw/baton/agents/<agentId>/model-allowlist.json`. Keep Baton state under `.openclaw/baton/`; never add Baton-only keys to `openclaw.json`.

Scripts: `baton-setup.mjs`; `baton-model-manager.mjs scan|list|add|remove|block|unblock|tier|prune-missing`; `baton-router.mjs route|release|cooldown|state`; `baton-status.mjs`; `baton-validate.mjs`. Conversation equivalents: rescan/show/allow/remove/block/tier models, set mode, show status.

When capacity is tight, serialize, spread providers, or collapse roles. Multiple main agents must pass `--agent-id <id>` and prefer per-agent state.

## Roles and tiers

Role families: control; research/analysis; content/creative; marketing/social; sales/support; product/design/dev; data/business/ops; education/media; agentic automation; safety/compliance. Consult `references/role-taxonomy.md` only when role choice is unclear.

Tier defaults: planner/validator/security/high-stakes=`strong_reasoning`; quick extraction=`fast`; research/support/ops=`balanced`; writing/social/campaigns=`creative`; code/automation/tool use=`code`; long docs=`long_context`; visual/PDF/image=`multimodal`.

## Safety gates

Dangerous or externally visible actions require explicit user authorization plus validator pass: sending/posting, deleting, deploying, modifying DNS/secrets/billing/production config, installs, payment, credentials, or high-stakes advice. Browser/tool/automation agents log actions and stop before irreversible external writes unless authorized.

## References

Read only when needed: `planner-orchestration`, `model-routing`, `rate-limits`, `model-management`, `model-discovery`, `role-taxonomy`, `patterns`, `permission-matrix`, `task-schema`, `prompts`, `resilience`, `conversation-management`.
