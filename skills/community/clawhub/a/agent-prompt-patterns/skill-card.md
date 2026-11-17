## Description:

Agent Prompt Patterns provides production-oriented prompt patterns for designing reliable AI agents and operating manuals, including validation, proof-of-work, approval tiers, heartbeat, contradiction detection, WAL, escalation, and cross-validation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to design, harden, and review production AI agent behavior and operating manuals. It is useful when defining approval tiers, completion criteria, validation loops, proof requirements, and safeguards for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may copy reference templates into an agent and treat them as automatic policy enforcement.

Mitigation: Review and adapt approval tiers before use, and add explicit human control or mechanical gates for sensitive actions.

Risk: Sensitive examples involve email sending, deletion outside the workspace, financial transactions, access-control changes, and public posting.

Mitigation: Keep these actions under explicit human approval and use the skill as guidance rather than an autonomous executor.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/skills/agent-prompt-patterns)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with example operating-manual snippets, code blocks, shell commands, and configuration patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no automatic policy enforcement or external service calls.]

## Skill Version(s):

98.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
