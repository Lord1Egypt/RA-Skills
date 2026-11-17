## Description:

Automate Brevo (Sendinblue) tasks via Rube MCP (Composio): manage email campaigns, create/edit templates, track senders, and monitor campaign performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Marketing operators, developers, and agents use this skill to manage Brevo email campaigns, templates, sender identities, and A/B testing workflows through Rube MCP. It helps agents find current tool schemas, connect to Brevo, and apply the right campaign or template parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to update Brevo campaigns or delete inactive templates, which could affect real marketing assets if the wrong item is selected.

Mitigation: Before updates or deletions, verify the exact campaign or template ID and name, then require explicit user confirmation.

Risk: Campaign or template changes may alter customer-facing email content, scheduling, recipients, or sender identity.

Mitigation: Review subject lines, HTML content or URLs, recipients, schedule, and verified sender details before allowing execution.

Risk: Using the skill requires connecting Rube MCP to a Brevo account, which gives the agent operational access to marketing assets.

Mitigation: Install and connect it only when that access is intended, and keep Brevo connection status and scope under user control.

## Reference(s):

- [Rube MCP endpoint](https://rube.app/mcp)
- [ClawHub skill page](https://clawhub.ai/sohamganatra/skills/brevo-automation)
- [ClawHub publisher profile](https://clawhub.ai/user/sohamganatra)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with tool names, parameter notes, workflow steps, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Rube MCP and an active Brevo connection; instructs the agent to search tools before using current schemas.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
