## Description:

AI Personal Assistant network skill for multi-agent PA coordination, including PA contact lookup, cross-agent coordination, owner-to-owner scheduling, PA group broadcasts, and local PA directory use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to coordinate through personal assistants, look up PA contacts from a local directory, arrange meetings, broadcast messages to PA groups, and prepare email or calendar actions on an owner's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive PA and owner contact details and can guide email, calendar, broadcast, or directory-write actions.

Mitigation: Require explicit owner approval before directory writes, calendar creation, email sends, broadcasts, or authentication setup.

Risk: The local context-loading example sources a shell file, which can execute arbitrary commands if the file is unsafe.

Mitigation: Replace shell sourcing with strict configuration parsing before deployment.

Risk: The declared contact source is inconsistent between PA_LIST.md and pa-directory.json, which can cause stale or incorrect coordination.

Mitigation: Align the production contact source and validate it before taking coordination actions.

Risk: One example directory includes real-looking contact details.

Mitigation: Remove real-looking example contacts and use placeholders or sanitized sample data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/ai-pa)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash, JSON, and command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local PA directory data and may produce contact, messaging, email, calendar, and directory-update instructions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
