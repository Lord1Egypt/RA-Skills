## Description:

Three-layer storage + four mechanisms + P0-P3 truth hierarchy for long-term agent memory. MEMORY.md central index, memory/core/ structured facts, local vector DB semantic search. Engramory curation, WAL protocol, context management. Zero external API, pure local filesystem + SQLite + LanceDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design local long-term memory for agents with a central MEMORY.md index, structured JSON facts, SQLite state, and local LanceDB semantic search. It is suited for persistent context, decision history, startup synchronization, and memory curation without external APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to create durable local agent memory and can persist profile, preference, strategy, session, portfolio, and account context.

Mitigation: Require explicit approval before enabling persistence, and add redaction, retention, deletion, and memory-review controls for sensitive use cases.

Risk: Automatic persistence of session and financial context may continue across startups without enough user control or protection details.

Mitigation: Review stored memory regularly, limit collection to necessary fields, and avoid enabling trading-related persistence unless the operator accepts the storage behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with directory layouts, checklists, and script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of durable local memory files, SQLite state, and local vector-search components.]

## Skill Version(s):

8.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
