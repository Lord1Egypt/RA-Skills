## Description:

Manage tasks, CRM leads, contacts, and settings via the DashTask REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sstrohl223](https://clawhub.ai/user/sstrohl223)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let AI agents manage DashTask tasks, projects, CRM records, contacts, quotes, notifications, and organization settings through the DashTask REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete business records and send emails through DashTask.

Mitigation: Use a least-privilege DashTask API key and require human approval before deletes, archive actions, settings changes, notifications, or email sends.

Risk: The skill depends on a configured DashTask endpoint and API key.

Mitigation: Install only when the endpoint is trusted and secrets are provided through the configured environment variables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sstrohl223/skills/dashtaREDACTED-SECRET)
- [DashTask](https://dashtask.ai)
- [OpenClaw](https://openclaw.ai)
- [SKILL.md API Reference](artifact/SKILL.md)
- [clawfile.json Manifest](artifact/clawfile.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payload examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHTASK_API_KEY and DASHTASK_ENDPOINT; outputs guide agents to make scoped DashTask API requests.]

## Skill Version(s):

1.9.1 (source: frontmatter, clawfile.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
