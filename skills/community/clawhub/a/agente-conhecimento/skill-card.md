## Description:

Logs and organizes learnings, errors, and feature requests so coding agents can preserve corrections, recurring failures, and useful project knowledge for later review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pedrohenrique202525](https://clawhub.ai/user/pedrohenrique202525)

### License/Terms of Use:


## Use Case:

Developers and coding-agent users use this skill to capture user corrections, command failures, knowledge gaps, and feature requests in structured Markdown logs. Teams can review those logs and promote durable lessons into project or agent instruction files after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs may capture secrets, personal data, prompts, error output, file paths, customer content, or proprietary information.

Mitigation: Apply strict redaction before writing logs and avoid storing sensitive conversation or environment details unless explicitly approved.

Risk: Promoting conversation-derived entries into future-session instruction files can change future agent behavior based on unreviewed or incorrect content.

Mitigation: Require explicit approval and human review before promoting learnings into persistent project or agent instruction files.

Risk: Optional hook setup references recurring scripts that were not included in the reviewed artifact.

Mitigation: Disable or avoid hook setup unless the referenced scripts are present, reviewed, and audited in the deployment environment.

Risk: Inter-session reading or sharing can expose content from other sessions.

Mitigation: Require explicit approval before reading other sessions or sending learnings across sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pedrohenrique202525/skills/agente-conhecimento)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured learning, error, and feature-request entries for agent-maintained Markdown files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
