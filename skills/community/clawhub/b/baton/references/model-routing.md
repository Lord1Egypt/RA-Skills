# Baton model routing

Baton routes by capability tier, role, execution mode, context need, risk, and shared rate-limit state. It should not hard-code provider preferences.

## Model resolution

Resolution order:

1. User per-request model/tier instruction.
2. Agent-specific `.openclaw/baton/agents/<agentId>/model-allowlist.json`.
3. Global `.openclaw/baton/model-allowlist.json`.
4. OpenClaw target-agent defaults.
5. OpenClaw global defaults.

Baton may pass `sessions_spawn.model` only if the selected ref is in the applicable Baton allowlist.

## Tier object schema

```json
{
  "tiers": {
    "fast": { "models": ["provider/model"], "fallback": "balanced", "maxAttempts": 2 },
    "balanced": { "models": [], "fallback": "strong_reasoning", "maxAttempts": 2 },
    "code": { "models": [], "fallback": "strong_reasoning", "maxAttempts": 2 },
    "long_context": { "models": [], "fallback": "strong_reasoning", "maxAttempts": 2 },
    "strong_reasoning": { "models": [], "fallback": null, "maxAttempts": 2 },
    "creative": { "models": [], "fallback": "balanced", "maxAttempts": 2 },
    "multimodal": { "models": [], "fallback": "long_context", "maxAttempts": 1 }
  }
}
```

## Workload to tier defaults

- `lookup`, `content_edit`, low-risk community replies, proofreading: `fast` if safe, otherwise `balanced`.
- `research`, `content_brief`, `sales_support`, `business_ops`, `product_design`: `balanced`.
- `deep_research`, `analysis`, `control`, `synthesis`, high-stakes review: `strong_reasoning`.
- `content_strategy`, `content_creation`, `marketing_growth`, `social_media`, `media_production`, `education_training`: `creative`, fallback `balanced`.
- `data_analysis`: `strong_reasoning` or `code` when computation/tools are needed.
- `code_edit`, integrations, automation builds, QA with tests: `code`, fallback `strong_reasoning`.
- `agentic_ops`: `strong_reasoning` or `code` depending on tools and external-risk level.
- `long_doc`: `long_context`.
- `multimodal`: `multimodal`.

## Role overrides

- Planner / Product Manager / Curriculum Designer: prefer `strong_reasoning`.
- Researcher / SEO Specialist / Competitive Analyst / UX Researcher: prefer `balanced`; `long_context` for large docs.
- Deep Researcher / Fact Checker / Domain Expert / Analyst: prefer `strong_reasoning`.
- Writer / Copywriter / Scriptwriter / Creative Director / Brand Strategist: prefer `creative`.
- Social Media Manager / Email Marketer / Paid Ads Specialist / PR-Comms Specialist: prefer `creative`; use `fast` for low-risk variants.
- Community Manager / Executive Assistant / Proofreader / File Clerk: prefer `fast` for low-risk work, otherwise `balanced`.
- Growth Marketer / Sales Development Rep / Customer Support Agent / Operations Analyst / Recruiter: prefer `balanced` or `creative` based on whether the output is analytical or copy-heavy.
- Data Analyst / QA Analyst / Tool Operator / Automation Agent / Integration Agent: prefer `code` when using computation, shell, or structured files.
- AI Agent / Browser Agent / Operator: prefer `strong_reasoning` with tool support; require explicit stop conditions.
- Art Director / Thumbnail Strategist / Vision Analyst: prefer `multimodal` when visual interpretation is needed.
- Validator / Compliance Reviewer / Security Reviewer / Brand Safety Reviewer: prefer `strong_reasoning`; when important, use a different provider or model family than the worker.
- Synthesiser: prefer `strong_reasoning` for multi-source or high-stakes synthesis.

## Rate-aware selection

Before spawning, check `.openclaw/baton/rate-limits.json` and `.openclaw/baton/runtime/rate-state.json` if available. Pick the first model that:

1. is allowed;
2. supports required context/tools/vision;
3. is not blocked or cooled down;
4. has capacity under provider/model concurrency limits;
5. has not repeatedly failed for the task type.

Spread parallel workers across providers/models when quality is similar.

## Escalation

Escalate when schema is malformed, tests fail, sources conflict, prompt-injection risk appears, a child reports capability limits, resolved model differs from requested model, or the task is high-risk.

## De-escalation

De-escalate for safe leaf work: formatting, extraction, title variants, deduplication, or low-risk content edits.

## Routing decision record

Append a JSONL row to `.openclaw/baton/model-routing-ledger.jsonl` when feasible:

```json
{
  "runId": "2026-06-13T12-00-00Z-abc123",
  "agentId": "main",
  "taskName": "validate_article_claims",
  "role": "Validator",
  "workloadClass": "research",
  "executionMode": "careful",
  "requestedTier": "strong_reasoning",
  "requestedModel": "provider/model",
  "resolvedModel": "provider/model",
  "provider": "provider",
  "fallbackUsed": false,
  "reason": "Independent factuality validation"
}
```
