---
name: agentic-codex-dev
description: Review agentic software-development plans and release readiness for Codex, GitHub, and ClawHub work. Use when a user asks for scoped delivery planning, implementation review, public-surface checks, or release evidence review without running remote-changing commands.
---

# Agentic Codex Dev

Use this skill as a text-only review layer for agentic development work. It helps turn a request, diff, repository note, or release checklist into a scoped plan and a conservative readiness verdict.

## Review Workflow

1. Restate the requested outcome and the smallest safe scope.
2. Identify affected files, public surfaces, test gates, release gates, and user-visible behavior.
3. Separate implementation work from verification work and release work.
4. Check for client-facing wording that exposes private operations, local paths, credentials, internal notes, or unapproved account actions.
5. Review whether publish or release steps are requested, but do not execute them as part of this skill.
6. Return a clear verdict: `ready`, `ready_with_notes`, `blocked`, or `do_not_ship`.

## Boundaries

- Do not request, print, store, or infer credentials.
- Do not stage, commit, push, publish, delete, hide, or transfer anything.
- Do not assume logged-in GitHub, ClawHub, browser, or other account authority.
- Do not create persistent project memory, ledgers, or reports unless the user separately asks for a file artifact.
- Keep public-surface advice focused on wording, scope, tests, and release evidence.

## Output Shape

Return:

- `Scope`: what is being reviewed.
- `Findings`: concrete issues ordered by severity.
- `Public surface`: wording or packaging risks.
- `Verification`: tests or checks that should pass before release.
- `Verdict`: one of `ready`, `ready_with_notes`, `blocked`, or `do_not_ship`.
