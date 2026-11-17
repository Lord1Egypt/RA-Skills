## Description:

Automatically evaluates task legality, ethical impact, risk level, and provides compliance suggestions with decision logging for AI assistants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betsymalthus](https://clawhub.ai/user/betsymalthus)

### License/Terms of Use:

MIT

## Use Case:

Developers, AI assistant operators, and compliance reviewers use this skill to screen proposed tasks for legal, privacy, security, and ethical risk before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision logging may retain full task descriptions and task details, which can include confidential, personal, legal, or security-sensitive information.

Mitigation: Disable decision logging or tightly control logs when sensitive task content may be processed.

Risk: Installation and update instructions reference mutable or inconsistent remote sources.

Mitigation: Install only a pinned, verified release from a single canonical source and avoid mutable global install or update commands where possible.

Risk: Automatic approval rules can allow risky tasks to proceed without enough review.

Mitigation: Keep human review enabled for non-trivial tasks and treat auto-approval rules as high-risk configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/betsymalthus/skills/claw-ethics-checker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, configuration snippets, and structured ethics-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record full task descriptions and task details in an in-memory decision log when decision logging is enabled.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
