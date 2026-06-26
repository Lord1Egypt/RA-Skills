# AANA Agent Memory Gate Skill

Use this skill when an OpenClaw-style agent may store, reuse, edit, summarize, infer, import, export, or delete user memory.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

User memory should be deliberate, relevant, accurate, reversible where possible, and approved before it is stored, reused, edited, or deleted.

The agent should separate:

- facts the user explicitly asked to remember,
- preferences the user clearly approved for future use,
- temporary task context that should not become memory,
- inferred traits that should not be stored without confirmation,
- sensitive information that should not be stored unless strictly necessary and explicitly approved,
- obsolete or incorrect memory that should be corrected or deleted with approval.

## When To Use

Use this skill before:

- saving a new user memory,
- reusing a stored memory to shape an answer or action,
- editing, merging, summarizing, or deleting existing memory,
- inferring preferences, identity details, relationships, locations, habits, health, legal, financial, employment, or personal facts,
- importing memory from files, messages, chats, notes, account records, or previous tasks,
- exporting or sharing memory with tools, services, collaborators, logs, prompts, or other agents.

## Memory Actions

Classify the proposed memory operation:

- `none`: no memory operation is needed.
- `read`: inspect memory for direct task relevance.
- `reuse`: use memory to personalize or constrain the current response.
- `store`: create a new memory.
- `edit`: correct, merge, narrow, or update a memory.
- `delete`: remove a memory.
- `export`: send memory outside the current agent context.
- `import`: add memory from another source.
- `unknown`: the memory operation is unclear.

## AANA Memory Gate Loop

1. Identify the current user request.
2. Identify the proposed memory operation.
3. Check relevance: is the memory needed for this task or future preference?
4. Check source: explicit user statement, user-approved preference, inferred, third-party, tool output, or unknown.
5. Check sensitivity: ordinary, personal, private, financial, health, legal, credential, biometric, child/minor, or protected-class information.
6. Check approval: explicit, implicit low-risk reuse, clarification needed, denied, or not needed.
7. Check lifecycle: should this be temporary, stored, updated, deleted, or never stored?
8. Choose action: proceed, ask, request approval, narrow, avoid storing, edit, delete, or refuse.

## Required Memory Checks

Before using memory, verify:

- user request,
- memory operation,
- memory content summary,
- source of the memory,
- why it is relevant,
- sensitivity class,
- approval status,
- retention or deletion expectation,
- whether a safer temporary-use alternative exists.

## Approval Rules

Require explicit user approval before:

- storing a new memory,
- editing, merging, or deleting memory,
- reusing sensitive memory for a new purpose,
- importing memory from another source,
- exporting memory outside the current agent context,
- storing inferred preferences or traits,
- storing anything about health, legal, financial, biometric, credential, child/minor, protected-class, or highly personal matters.

Approval should name the exact memory action and compact content:

```text
Should I remember that you prefer concise status updates for this project?
```

Do not treat silence as approval.

## Reuse Rules

Reuse memory only when:

- it is relevant to the current request,
- it was stored with user approval or is low-risk task preference memory,
- it does not introduce unrelated private data,
- it does not override the user's current instruction,
- it is not stale, conflicting, or likely incorrect.

Ask before reuse when:

- the memory is sensitive,
- the memory conflicts with the current request,
- the memory was inferred rather than explicitly provided,
- the memory comes from another context, account, user, or tool source,
- the user may not expect it to affect this task.

## Storage Rules

Do not store:

- secrets, passwords, API keys, private keys, tokens, cookies, or security codes,
- payment numbers, bank details, government IDs, medical records, legal records, raw financial records,
- full private messages, full logs, full transcripts, or unrelated personal data,
- protected-class traits, biometric data, child/minor data, trauma details, or intimate details unless explicitly requested and appropriate,
- speculative inferences, labels, diagnoses, risk scores, or judgments about the user,
- temporary task context that is only needed for the current request.

Prefer:

- short user-approved preferences,
- project-specific working notes with clear scope,
- redacted summaries,
- time-limited notes,
- asking before storage.

## Edit And Delete Rules

Before editing or deleting memory:

- show or summarize the memory being changed,
- explain the proposed edit or deletion,
- get explicit approval,
- avoid deleting broad groups of memories unless the user clearly requested that scope.

If a memory is wrong, stale, sensitive, or no longer wanted, ask whether to correct, narrow, or delete it.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `user_request`
- `memory_operation`
- `memory_summary`
- `source_status`
- `relevance_status`
- `sensitivity_status`
- `approval_status`
- `lifecycle_status`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full account records, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If no memory is needed, do not use memory.
- If low-risk memory is relevant and approved for this purpose, reuse it.
- If storing, editing, deleting, importing, exporting, or sensitive reuse is proposed, request explicit approval.
- If the content is sensitive or unnecessary, avoid storing and use temporary context only.
- If the memory is stale, conflicting, or unsupported, ask before using or changing it.
- If the memory action would expose secrets, violate consent, or misuse private data, refuse that part.
- If a checker is unavailable or untrusted, use manual memory review.

## Output Pattern

For memory-sensitive work, prefer:

```text
AANA memory gate:
- Request: ...
- Memory operation: none / read / reuse / store / edit / delete / export / import / unknown
- Memory summary: ...
- Source: explicit_user / approved_preference / inferred / third_party / tool_output / unknown
- Relevance: relevant / partial / unrelated / unknown
- Sensitivity: ordinary / personal / private / financial / health / legal / credential / protected / unknown
- Approval: explicit / implicit_low_risk / required / denied / unclear
- Decision: proceed / ask / request_approval / narrow / avoid_storing / edit / delete / refuse
```

Do not include this gate in the user-facing answer unless approval, correction, deletion, or a memory boundary needs to be explained.
