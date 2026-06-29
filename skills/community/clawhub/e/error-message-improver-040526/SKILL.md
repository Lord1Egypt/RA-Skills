---
name: error-message-improver
description: >-
  Rewrite vague application, API, CLI, and support errors into diagnostic messages that explain what failed, why it likely failed, and the next safe action. Use when a user asks for error messages, debugging, support, validation, user feedback, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# Error Message Improver

## Purpose

Use this skill when an error string, exception payload, validation response, or support macro is technically correct but not actionable. It turns failure states into messages with cause, impact, recovery, and escalation detail while preserving accuracy.

Audience: product engineers, platform teams, support leads, technical writers, and SaaS operators who need errors that reduce tickets and unblock users.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Collect the original error, operation, affected role, logs or status codes, and constraints around tone, localization, security, or legal wording.
2. Classify the failure as validation, permission, dependency, rate limit, data conflict, timeout, unavailable service, configuration, or unknown internal error.
3. Draft the message in layers: user-facing summary, concrete reason, recovery action, durable reference code, and optional support/debug detail.
4. Remove blame, speculation, stack traces, secrets, and implementation names that do not help the user act safely.
5. Add developer or support notes for logging fields, telemetry dimensions, docs links, or runbook handoff.
6. Check that a user can tell what happened, whether retrying is useful, and what to do next.

## Expected Outputs

- A before-and-after error message rewrite with rationale.
- A structured error payload or copy pattern.
- Telemetry and support fields for recurring failures.
- A checklist for reviewing similar messages across a codebase.

## Validation

- The rewritten message names the failure and next action without inventing facts.
- Sensitive internals, secrets, and irrelevant stack traces are excluded.
- Recovery guidance distinguishes retry, user fix, admin fix, and support escalation.
- The result can be implemented as copy, code constants, API responses, or docs.

## Triggers

Keywords: `error messages`, `debugging`, `support`, `validation`, `user feedback`, `troubleshooting`, `copywriting`

Example trigger sentences:

- `Use $error-message-improver to rewrite this API error so customers know what to fix.`
- `This CLI failure is vague; make it actionable without exposing internals.`
- `Create an error-message checklist for our signup and billing flows.`
