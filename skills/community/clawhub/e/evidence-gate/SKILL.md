---
name: "evidence-gate"
description: "Generates evidence obligations for a claim or action, evaluates existing evidence against them, and returns a structured verdict (PASS / SOFT_PASS / BLOCK / CONFLICT) with safe downgrade guidance. TRIGGER when the agent is about to present a root-cause diagnosis, claim 'the cause is X', say 'this is safe', recommend a destructive or irreversible action, recommend a rollback, make a safety assertion, or state a strong conclusion based on limited evidence. DO NOT TRIGGER when summarizing, formatting, brainstorming possibilities, performing low-risk reversible operations, or when the caller already has its own evidence-validation step."
---

# Evidence Gate

Use this skill to insert a lightweight evidence gate into an existing workflow without replacing the workflow.

Its purpose is not to make the caller more cautious — capable agents are already cautious.
Its purpose is to make that caution **structured, auditable, and actionable** by answering a narrower question:

**What evidence must exist before this conclusion or action is responsible enough to present, recommend, or execute?**

Treat the caller's conclusion or action as tentative until the gate returns a verdict.

Keep the skill lightweight, selective, and non-blocking by default.

## Scope

This skill gates the agent's own reasoning quality — not the user's intent.

It is not:
- content moderation or policy enforcement
- user intent classification (allow / refuse / clarify)
- a legal, compliance, or safety advisory tool
- a replacement for domain expertise

## Core idea

Given a tentative claim or action, do three things:

1. Define the minimum evidence obligations for that claim/action.
2. Check what evidence already exists and what is still missing or conflicting.
3. Return a verdict and a safe next-step policy.

Do not fully own evidence collection.
Recommend missing evidence for the caller to gather using its existing tools.

## Operating model

Use a single-pass gate instead of taking over the full workflow:

1. The caller reaches a tentative claim, diagnosis, recommendation, or action.
2. Generate the evidence obligations for that candidate.
3. Evaluate only the evidence currently available in the invocation.
4. Return a final verdict for this invocation:
   - whether the current evidence is sufficient
   - how the caller should downgrade if it is not
   - which next evidence checks would be most valuable
5. Exit.

Assume no durable skill state across calls.
Do not require a second gate pass unless the caller explicitly chooses to orchestrate one outside this skill.

## When to use

Use this skill when one or more of the following are true:

- The caller is about to make a strong claim such as:
  - "the root cause is X"
  - "this is safe"
  - "this configuration should be changed"
  - "the correct action is Y"
- The caller is about to recommend or execute a high-impact step such as:
  - rollback
  - scale up/down
  - delete/disable/quarantine
  - approve/reject
  - change production configuration
- The current conclusion appears to rely on only one signal, one log line, one chart, or one tool result.
- Competing explanations have not been checked.
- The user explicitly asks for an evidence-backed answer.
- The environment or workflow has a policy requiring stronger justification before action.

## When NOT to use

Do not use this skill when:

- The output is low-risk and easily reversible.
- The task is simple summarization or formatting.
- The caller is brainstorming possibilities and is not presenting a conclusion as established.
- The additional delay or cost of gating would outweigh the value.
- The caller already has an explicit evidence-validation layer for this exact step.

## Design constraints

This skill must preserve the caller's original capability as much as possible.

It should:
- be selective rather than always-on
- avoid taking over the entire workflow
- avoid forcing chain-of-thought disclosure
- avoid blocking work unless a real risk threshold is crossed
- prefer downgrade/fallback over hard failure
- assume each invocation is stateless

## Integration policy

Apply these defaults unless the caller provides stricter policy:

1. Run the gate only at conclusion points or before high-impact actions.
2. Generate only `2-5` concrete evidence obligations.
3. Evaluate only the evidence explicitly present in the current invocation.
4. Return one final verdict for the current invocation.
5. If evidence is insufficient, downgrade or defer instead of spinning.
6. Keep domain ownership with the caller.
7. Judge only explicit artifacts, not hidden reasoning.

## Input contract

The only required input is the **claim** — the conclusion, diagnosis, recommendation, or action under consideration.

Invocation examples:

- `/evidence-gate "The root cause is a nil dereference in request parsing"`
- `/evidence-gate "Safe to delete the staging database"`
- Agent self-trigger: the agent recognizes a gate-worthy moment and invokes the skill with the current claim from context.

When invoked with just a claim, the skill infers the remaining context:

- `claim_type`: inferred from the claim language (e.g., "the cause is" → `diagnosis`, "safe to" → `safety`, "should delete" → `action`)
- `domain`: inferred from the current working context
- `risk_level`: inferred from the action's reversibility and blast radius
- `execution_mode`: inferred from whether the caller is informing, recommending, or about to execute
- `target_strength`: inferred from the claim's language strength

The caller may optionally provide any of these fields to override inference.
Use `references/input-template.md` when a caller wants a canonical explicit input shape.
See `references/protocol.md` for the full schema semantics.

## Output contract

The skill should return a structured gate result containing:

- whether a gate is required
- why the gate is required
- evidence requirements
- per-requirement status
- missing evidence
- conflicting evidence
- sufficiency rule
- verdict
- allowed next actions
- blocked next actions
- fallback behavior
- suggested caller wording when evidence is insufficient
- next evidence actions

Return JSON matching `references/output-template.md`.
Use `references/verdict-schema.json` as the machine-checkable schema.
Keep `gate_required` even on explicit invocation.
Use `gate_required = false` as a fast exit when the claim is already low-risk, exploratory, or sufficiently bounded.

## Verdict states

Use exactly these verdicts:

- `PASS`
  - Evidence is sufficient for the intended claim/action.
- `SOFT_PASS`
  - Evidence is incomplete, but sufficient for a weaker claim, advisory output, or low-risk continuation.
- `BLOCK`
  - Evidence is insufficient for the intended strength or risk level. High-impact continuation should not proceed.
- `CONFLICT`
  - Evidence materially disagrees or supports multiple competing interpretations. The caller should not present a strong conclusion as settled.

## Required behavior

### 1. Normalize the candidate
Reduce the caller's current position to a tentative, explicit candidate.
If the caller already states the final conclusion as settled, rewrite it internally as tentative before gating it.

### 2. Define evidence obligations
Translate the candidate claim/action into a small set of concrete evidence requirements.

Good evidence requirements are:
- specific
- externally checkable
- operationally gatherable
- tied to the claim, not generic boilerplate

Bad evidence requirements are vague, such as:
- "get more proof"
- "verify better"
- "be more certain"

### 3. Evaluate sufficiency
Determine whether currently known evidence satisfies the requirements.

The skill should explicitly mark:
- `satisfied`
- `missing`
- `conflicting`
- `not_applicable`

### 4. Produce a final verdict for the current invocation
Return a verdict immediately after evaluating known evidence.
If evidence is missing, identify only the smallest set of additional checks that would materially change the verdict.

### 5. Prefer downgrade over dead stop
If evidence is insufficient, prefer one of:
- provisional conclusion
- candidate hypotheses
- advisory-only output
- ask-for-human-review
- request-more-evidence plan

Do not hard-block low-risk work unnecessarily.

### 6. Assume stateless execution
Assume every call is fresh.
Do not depend on remembering prior requirements, prior verdicts, or prior collection attempts unless the caller explicitly embeds them in the current input.

### 7. Avoid hidden-reasoning dependence
Do not require access to hidden chain-of-thought.
Judge only from explicit claim, explicit evidence, explicit policy, and explicit outputs.

## Suggested workflow

1. Receive normalized candidate claim/action.
2. Decide whether gating is required.
3. If no gate is required, return `PASS` with rationale.
4. If a gate is required:
   - generate evidence requirements
   - evaluate known evidence
   - identify gaps and conflicts
   - apply a sufficiency rule
   - produce a final verdict for this invocation
   - produce fallback and next-step guidance
5. Return a structured result without taking over execution.

## Default trigger heuristics

Bias toward using this skill when any of the following are present:

- `risk_level = high`
- `execution_mode = auto`
- claim language is strong or definitive
- only one evidence source supports the claim
- no competing hypothesis check exists
- action is costly, irreversible, or externally visible

Bias away from using this skill when:

- `risk_level = low`
- the output is exploratory, not conclusive
- the result is easy to reverse
- the task is primarily formatting or summarization

## Default fallback policy

When the gate does not fully pass, prefer these downgrades:

- intended strong conclusion -> provisional conclusion
- automatic action -> advisory recommendation
- settled diagnosis -> candidate hypotheses
- irreversible operation -> human approval required
- insufficient current evidence -> stop and return a bounded next-evidence plan

## Output style guidance

When the verdict is not `PASS`, the caller should avoid overstating certainty.

Good examples:
- "Current evidence suggests X, but this is not yet sufficiently established."
- "This is a plausible diagnosis, not a confirmed root cause."
- "Evidence is currently insufficient for automatic execution."
- "Additional evidence is needed before recommending Y with confidence."

Bad examples:
- "This is definitely the cause" when key evidence is missing
- "Safe to proceed" when competing evidence exists

## Example use cases

- SRE:
  Before recommending scale-up, verify that bottleneck evidence is real and alternative explanations were checked.
- Coding:
  Before claiming a bug root cause, verify reproduction path, code-path match, and at least one falsified alternative.
- Security:
  Before declaring an action safe, require policy match, scope confirmation, and risk checks.
- Research:
  Before presenting a strong conclusion, require source support and contradiction checks.

## Non-goals

This skill is not:
- a universal orchestrator
- a replacement for domain expertise
- a guarantee of correctness
- a hidden chain-of-thought inspector
- a mandatory wrapper around every agent step

Its job is narrower:
**make evidence obligations explicit, assess whether they are met, and enforce safe downgrade behavior when they are not.**
