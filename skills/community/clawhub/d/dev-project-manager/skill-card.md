## Description:

Dev Project Manager guides a PM agent through software requirements, SRS drafting, change control, estimation, Asana-backed task coordination, stakeholder updates, implementation plan review, and heartbeat queue checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and operator-managed agent teams use this skill to turn client requirements into structured project artifacts, coordinate engineering assessment and implementation planning, maintain Asana/project state, and keep stakeholders updated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect project records and Asana task state through dependency skills.

Mitigation: Install it only on a PM agent intended to manage the named OpenClaw projects, and verify USER.md, HEARTBEAT.md, AGENTS.md, and dependency skills before use.

Risk: Incorrect project identifiers or agent mappings can route work or nudges to the wrong project team.

Mitigation: Confirm workspace files point to the intended projects, queues, agents, and Asana sections before triggering active project-management workflows.

## Reference(s):

- [Dev Project Manager Skill](https://clawhub.ai/encryptshawn/skills/dev-project-manager)
- [SRS Standard](references/srs_standard.md)
- [PM Communication Templates](references/templates.md)
- [Engineer Communication Protocols](references/engineer_protocols.md)
- [Requirements Elicitation Framework](references/requirements_elicitation.md)
- [Estimation & Effort Communication Guide](references/estimation.md)
- [Change Management & Scope Control](references/change_management.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, structured text, and JSON-compatible project state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include SRS drafts, requirements summaries, change request records, stakeholder updates, queue messages, task setup guidance, and project state changes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
