## Description:

Local-first persistent memory for AI agents with SQLite storage, orchestrated retrieve/extract loops, hybrid retrieval, contradiction checks, correction learning, and optional SuperMemory mirroring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dobrinalexandru](https://clawhub.ai/user/dobrinalexandru)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Agent Brain to give AI agents persistent local memory, retrieve relevant context, detect contradictions, and learn from corrections across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build long-lived memory about a user and their projects.

Mitigation: Install only when persistent memory is intended, review or disable automatic extraction, and inspect exported memory regularly.

Risk: Full memory entries can be mirrored to a cloud endpoint when credentials and sync configuration are present.

Mitigation: Set AGENT_BRAIN_SUPERMEMORY_SYNC=off unless cloud mirroring is explicitly approved and required.

Risk: Secrets, regulated data, superseded entries, and logged information can remain durable once stored.

Mitigation: Avoid storing secrets or regulated data and periodically review memory exports for sensitive or stale content.

## Reference(s):

- [ClawHub Agent Brain release page](https://clawhub.ai/dobrinalexandru/skills/agent-brain)
- [Project homepage listed in skill metadata](https://github.com/alexdobri/agent-brain)
- [Optional SuperMemory API endpoint](https://api.supermemory.ai/v3/documents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local script invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create, retrieve, update, export, and optionally mirror persistent memory entries depending on user-approved configuration.]

## Skill Version(s):

1.0.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
