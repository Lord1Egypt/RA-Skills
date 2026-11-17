## Description:

Connect to 100+ APIs, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot, through Maton's managed OAuth API gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation agents use this skill to call native third-party API endpoints through Maton-managed connections. It is suited for workflows that need authenticated read, write, or delete actions across supported SaaS services after the user authorizes each service connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad read, write, and delete actions across Maton-connected services.

Mitigation: Authorize only the services needed for the task, use narrowly scoped connections where available, and manually confirm destructive or public-posting actions.

Risk: The MATON_API_KEY can be exposed through logs, transcripts, or unsafe troubleshooting output.

Mitigation: Do not print, paste, or store the key in conversation history or shared logs; rotate the key if exposure is suspected.

Risk: Financial or administrative service connections could increase operational impact if misused.

Mitigation: Avoid granting financial or admin account access unless necessary, and prefer dedicated least-privilege accounts for agent workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/skills/19-api-gateway)
- [Maton Homepage](https://maton.ai)
- [API Gateway Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline JSON and Python or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a MATON_API_KEY environment variable; third-party service access also requires user-authorized Maton connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
