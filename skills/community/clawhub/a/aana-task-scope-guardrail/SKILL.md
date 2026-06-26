# AANA Task Scope Guardrail Skill

Use this skill when an OpenClaw-style agent may expand beyond the user's requested task, use unrelated data, continue after completion, or keep acting after the goal has already been satisfied.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

The agent should do the requested task, use only task-relevant context, and stop when the request is complete.

The agent should separate:

- work that is explicitly requested,
- work that is required to complete the request,
- optional follow-up suggestions,
- unrelated work that should not be done,
- sensitive or unrelated data that should not be used,
- continuing behavior that should stop.

## When To Use

Use this skill before:

- expanding a task into extra research, cleanup, refactoring, outreach, browsing, data access, or tool use,
- reading unrelated files, messages, repositories, account records, tickets, logs, or personal data,
- continuing after the requested answer, edit, review, booking, purchase, file operation, or tool action is complete,
- starting adjacent tasks because they seem helpful but were not requested,
- retaining, summarizing, or reusing private context from another task,
- making follow-up changes after the user asked for a narrow patch, answer, or decision.

## Scope Categories

Classify the proposed action:

- `in_scope`: directly requested by the user.
- `necessary_support`: required to complete the requested task safely.
- `clarification_needed`: the task boundary is ambiguous.
- `optional_followup`: useful but not required; mention briefly without doing it.
- `out_of_scope`: unrelated, premature, or beyond the requested boundary.
- `stop`: the request is complete and the agent should not keep acting.

## AANA Scope Gate Loop

1. Identify the user's current request.
2. State the smallest useful completion target.
3. Identify the proposed next action.
4. Check whether the action is requested, necessary, optional, unrelated, or already complete.
5. Check whether the action uses only task-relevant data.
6. Check whether it needs extra authorization because it changes scope, accesses private data, or affects external state.
7. Choose action: proceed, narrow, ask, suggest, stop, or refuse.

## Required Scope Checks

Before doing more work, verify:

- current user request,
- completion target,
- proposed next action,
- relationship to the request,
- data needed and why it is relevant,
- whether the action changes systems, files, messages, money, accounts, or public content,
- whether the user has authorized that scope,
- whether the request is already complete.

## Task Expansion Rules

Do not expand the task when:

- the user asked for a narrow answer, patch, review, or example,
- the extra work is only adjacent or potentially useful,
- the extra work requires new tools, private data, external actions, or broad searches,
- the agent would change files, settings, accounts, or public content beyond the requested target,
- the agent would start a new project phase without user approval.

Ask before expanding when:

- the next step would materially change scope,
- multiple reasonable interpretations exist,
- the request implies a risky or high-impact follow-up,
- the work would require unrelated data or broad context access.

## Data Relevance Rules

Use only data that is needed for the current task.

Do not use:

- unrelated private messages, files, logs, account records, or histories,
- secrets, credentials, payment data, health/legal/financial records, or personal data unless required and authorized,
- context from another user, another account, another repository, or another task,
- old task context when the current request has moved on.

Prefer:

- minimal snippets,
- redacted summaries,
- task-specific files,
- direct user-provided evidence,
- narrow queries and exact targets.

## Completion Rules

Stop when:

- the requested answer has been given,
- the requested edit or artifact has been created,
- the requested validation has been run and reported,
- the requested decision has been routed or made,
- the user asked for status only and status has been provided,
- continuing would require a new task or approval.

After completion, do not keep using tools, reading data, making changes, or running extra checks unless the user requested it or the remaining check is part of the agreed task.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `user_request`
- `completion_target`
- `proposed_next_action`
- `scope_status`
- `data_relevance_status`
- `authorization_status`
- `completion_status`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full directory dumps, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If the action is requested, necessary, authorized, and uses task-relevant data, proceed.
- If the action is useful but broader than needed, narrow it.
- If the boundary is ambiguous, ask the user.
- If the work is optional, mention it as a follow-up without doing it.
- If the task is complete, stop.
- If the action uses unrelated data, changes scope without approval, or keeps operating after completion, refuse or defer that part.
- If a checker is unavailable or untrusted, use manual task-scope review.

## Output Pattern

For scope-sensitive work, prefer:

```text
AANA scope gate:
- Request: ...
- Completion target: ...
- Proposed next action: ...
- Scope: in_scope / necessary_support / clarification_needed / optional_followup / out_of_scope / stop
- Data relevance: relevant / partly_relevant / unrelated / sensitive_extra_data / unknown
- Authorization: explicit / implicit_for_task / clarification_needed / not_authorized
- Decision: proceed / narrow / ask / suggest / stop / refuse
```

Do not include this gate in the user-facing answer unless clarification, approval, or a scope boundary needs to be explained.
