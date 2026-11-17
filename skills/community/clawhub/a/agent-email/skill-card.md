## Description:

Enables outbound email notifications through AgentMail.to for system alerts and task completion reports using thundarr@agentmail.to.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrslu01](https://clawhub.ai/user/zrslu01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent to send outbound email alerts, such as system health notifications, threshold alerts, and task completion reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send outbound email through AgentMail.to when configured with an API key.

Mitigation: Install only when outbound email is intended, protect the API key, and verify recipients before sending.

Risk: The artifact references send_mail.py, but that script is not included in the packaged files.

Mitigation: Confirm the delivery script or equivalent tool is present and reviewed in the deployment environment before relying on the skill.

## Reference(s):

- [Agent Email on ClawHub](https://clawhub.ai/zrslu01/skills/agent-email)
- [Publisher profile](https://clawhub.ai/user/zrslu01)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance for configuring and invoking outbound email delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid AgentMail API key and recipient verification before sending.]

## Skill Version(s):

1.0.0 (source: skill.yaml and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
