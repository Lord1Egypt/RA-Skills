## Description:

Spawns a Bailian (DashScope) subagent to handle token-heavy or compute-intensive work such as data processing, batch operations, SQL execution, news fetching, code generation, and document analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelhsin](https://clawhub.ai/user/samuelhsin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to delegate large, repetitive, or token-heavy tasks to a Bailian model while keeping final decisions, sensitive judgment, and user-facing conversation with the main agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may include raw access keys, session tokens, passwords, or production database authority when delegating work to Bailian.

Mitigation: Keep credentials out of model text and use short-lived, read-only, scoped credentials handled outside the prompt.

Risk: Delegated database work may include SQL writes, schema changes, or destructive operations without clear safeguards.

Mitigation: Require explicit review before any SQL write, schema change, or destructive operation.

Risk: Subagent output may be incorrect or incomplete for final user-facing decisions.

Mitigation: Use the main agent to review delegated results before acting on them or presenting final guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuelhsin/skills/bailian-subagent)
- [Publisher profile](https://clawhub.ai/user/samuelhsin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code and command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated subagent output should be reviewed by the main agent before final use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
