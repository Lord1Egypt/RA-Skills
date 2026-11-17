## Description:

Automate Calendly scheduling, event management, invitee tracking, availability checks, and organization administration via Rube MCP (Composio). Always search tools first for current schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide agents through Calendly workflows, including event lookup, invitee management, scheduling link creation, availability checks, cancellation, and organization administration through Rube MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendly OAuth access can expose calendar and organization workflows through Rube MCP.

Mitigation: Trust the Rube MCP/Composio connection before installation and authorize only the Calendly scopes needed.

Risk: Cancellation and organization-management actions can affect invitees or account membership.

Mitigation: Confirm destructive or administrative actions with the user before executing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sohamganatra/skills/calendly-automation)
- [Rube MCP Endpoint](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with ordered tool sequences and parameter notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Rube MCP with an active Calendly OAuth connection; recommends searching tools first for current schemas.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
