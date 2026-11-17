## Description:

Agent Org Manager helps teams structure multi-agent organizations with rosters, three-channel communication, daily reporting, autonomous learning, and audit routines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygq19901001](https://clawhub.ai/user/ygq19901001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing three or more agents use this skill to define departmental roles, communication routes, scheduled learning and reporting, and inspection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ready-to-deploy scheduled jobs can automatically publish skills and modify GitHub releases without clear human approval controls.

Mitigation: Gate publishing and release-modification jobs behind human approval, repository allowlists, diff review, and least-privilege credentials.

Risk: Repair-task error text can be treated as instructions by repair agents.

Mitigation: Treat error text as untrusted data and limit repair agents to the specific job and fields being fixed.

## Reference(s):

- [Communication Patterns](references/communication-patterns.md)
- [Cron Templates](references/cron-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/ygq19901001/skills/agent-org-manager)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON cron templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes replaceable placeholders for department names, schedules, models, alert channels, and output paths.]

## Skill Version(s):

1.0.0 (source: target metadata and server release metadata; artifact frontmatter lists 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
