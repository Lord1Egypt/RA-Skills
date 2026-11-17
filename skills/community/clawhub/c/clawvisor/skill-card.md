## Description:

Route tool requests through Clawvisor for credential vaulting, task-scoped authorization, and human approval flows for Gmail, Calendar, Drive, Contacts, GitHub, and iMessage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlevine](https://clawhub.ai/user/ericlevine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route service actions through Clawvisor so credentials stay vaulted, task scopes are approved, restrictions are enforced, and risky actions can require human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent token is a high-privilege credential for services activated in Clawvisor.

Mitigation: Use a dedicated scoped token, keep task scopes narrow, and rotate or revoke the token immediately if it is exposed.

Risk: Standing or broad task scopes can permit persistent access to sensitive Gmail, Calendar, Drive, Contacts, GitHub, or iMessage data.

Mitigation: Prefer short-lived tasks, avoid standing all-mailbox authorizations unless necessary, and use session identifiers for standing workflows.

Risk: Write or destructive service actions can affect email, calendar events, files, issues, or messages.

Mitigation: Review and apply the included safe policies so writes and sensitive reads require approval, email deletion is blocked, and iMessage sending remains disabled unless explicitly enabled.

Risk: Self-hosted Clawvisor setup commands depend on the deployed service version and trust boundary.

Mitigation: Pin or verify the self-hosted Clawvisor version before running setup commands and install only when the Clawvisor deployment is trusted.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ericlevine/skills/clawvisor)
- [Clawvisor repository](https://github.com/clawvisor/clawvisor)
- [Task and request examples](https://github.com/clawvisor/clawvisor/blob/main/docs/TASK_EXAMPLES.md)
- [Clawvisor docs](https://github.com/clawvisor/clawvisor/tree/main/docs)
- [Clawvisor hosted access](https://clawvisor.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWVISOR_URL, CLAWVISOR_AGENT_TOKEN, and OPENCLAW_HOOKS_URL; routes service actions through Clawvisor task scopes, restrictions, and approval flows.]

## Skill Version(s):

0.9.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
