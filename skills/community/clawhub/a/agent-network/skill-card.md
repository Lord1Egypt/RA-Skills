## Description:

Agent Network provides a local multi-agent collaboration system with group chat, mentions, task assignment, decision voting, inbox notifications, and SQLite-backed coordination records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtimeschange](https://clawhub.ai/user/howtimeschange)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add local multi-agent collaboration workflows with group chat, mentions, task assignment, decision voting, inbox notifications, and SQLite-backed coordination records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Any caller with package access can impersonate agents or read, alter, or delete shared collaboration records because the skill lacks access controls.

Mitigation: Use only in trusted, local or single-operator workflows until authentication, authorization, membership checks, audit logging, scoped reads, and deletion recovery controls are added.

Risk: Webhook and state-persistence examples may expose sensitive collaboration content if adapted directly.

Mitigation: Harden integrations before use with sensitive content, including secret handling, destination validation, access scoping, and review of persisted data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtimeschange/skills/agent-network)
- [Advanced Usage Guide](references/ADVANCED.md)
- [Database Schema](references/schema.sql)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run local scripts and persist collaboration state in SQLite.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
