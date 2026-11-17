## Description:

Classifies OpenClaw operations by CRUD category, allowing read operations without additional approval while requiring confirmation before create, update, edit, or delete actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uynewnas](https://clawhub.ai/user/uynewnas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to apply a persistent approval workflow where read-only operations proceed quickly and write or deletion operations require a visible confirmation step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permits file reads, searches, and directory browsing without a second confirmation, which can expose secrets, credentials, logs, private repositories, or other sensitive files in permissive environments.

Mitigation: Install only where unrestricted read access is acceptable, or modify the workflow to require explicit approval before reading or searching sensitive paths and data types.

Risk: A persistent CRUD approval workflow may weaken stricter local review expectations by treating read operations as automatically safe across sessions.

Mitigation: Review the skill before deployment and keep platform, workspace, and tool-level permission boundaries in force for sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/uynewnas/skills/crud)
- [OpenClaw Official Documentation](https://docs.openclaw.ai/)
- [Reference Project](https://github.com/peterskoett/self-improving-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown operational guidance and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No additional configuration files are required by the artifact documentation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
