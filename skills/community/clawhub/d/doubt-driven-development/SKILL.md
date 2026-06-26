---
name: doubt-driven-development
description: "Stress-test high-risk changes with fresh-context skepticism before implementation or release. Use when work involves production, permissions, security controls, public packages, data deletion or migration, billing, credentials handling, irreversible operations, CI failures that are hard to explain, or any task where a confident but wrong agent answer would be costly."
---

# Doubt Driven Development

Use this skill to slow down only where being wrong is expensive. The goal is not pessimism; the goal is to make the riskiest assumption visible and testable.

## Workflow

1. **Name the claim**
   - Write the proposed change or decision as one falsifiable sentence.
   - Example: `Publishing this skill version is safe because validation and CI cover the release surface.`

2. **List failure modes**
   - What would make the claim false?
   - Include behavior, tests, release metadata, permissions, secrets handling, and rollback paths.

3. **Seek disconfirming evidence**
   - Read the smallest relevant code, docs, config, logs, CI output, and release artifacts.
   - Prefer direct evidence over confidence, memory, or broad statements.

4. **Force a safer alternative**
   - If evidence is weak, choose a smaller change, add a check, or stop for user decision.
   - Do not proceed by relying on trust in the agent's prior answer.

5. **Decide**
   - `proceed`: evidence supports the claim and verification passed.
   - `patch first`: fix a concrete gap before shipping.
   - `stop`: risk is unresolved or requires user judgment.

## Fresh-Context Review

Use an isolated review pass when the blast radius is high and the runtime supports it. The reviewer should receive the artifact and task, not your intended conclusion.

Good review prompt shape:

```text
Review this change for release-blocking correctness, test, and security issues. Focus on concrete defects and cite files or commands.
```

Avoid prompts that disclose the expected answer or ask the reviewer to validate your plan.

## Risk Signals

Escalate scrutiny when you see:

- Broad permissions or sandbox changes.
- Network publishing, package release, or public registry updates.
- Handling of tokens, private user data, or local credential stores.
- Destructive file, database, cloud, or infrastructure commands.
- Large generated diffs with little reviewable structure.
- CI failures that were fixed by retrying without root cause.
- Claims like "obviously safe", "only docs", or "no tests needed" on release paths.

## Sandbox Review Posture

For Codex sandbox, approval, and policy work, treat review as a boundary check, not a permission grant. Auto-review can decide whether a boundary-crossing action should run, but it does not expand writable roots, enable network access, or weaken protected paths.

When mundane work keeps needing approval, prefer a narrower boundary fix such as a specific writable root or exact command prefix. Do not solve noisy review traffic by making broad rules that remove the boundary being reviewed.

## Output Template

```text
Claim: <falsifiable claim>
Main risk: <highest-impact failure mode>
Evidence checked: <files, tests, CI, docs>
Decision: proceed | patch first | stop
Reason: <short concrete rationale>
```

Keep the output terse. If the decision is `patch first` or `stop`, name the next concrete action.
