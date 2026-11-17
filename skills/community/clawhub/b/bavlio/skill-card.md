## Description:

Run lead discovery and outreach through Bavlio, the AI SDR that researches every lead before it writes. Plan and run lead searches, enrich datasets, write campaign copy, and manage LinkedIn plus email sequences via the Bavlio MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bavlio](https://clawhub.ai/user/bavlio)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, and developers use this skill to connect an agent to a Bavlio workspace for lead discovery, enrichment, campaign preparation, and unified inbox review across LinkedIn and email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead searches and enrichment can spend Bavlio credits.

Mitigation: Show the plan and maximum credit charge, then require explicit user confirmation before running paid searches or enrichment.

Risk: Campaign launch can send outreach through connected email and LinkedIn identities.

Mitigation: Require user approval of the final audience, sender identities, sequence, and message copy before launching a campaign.

Risk: The Bavlio API key allows an agent to operate the connected workspace.

Mitigation: Install only for intended Bavlio workspaces and keep the API key in an environment variable or other managed secret store.

## Reference(s):

- [Bavlio documentation](https://bavlio.com/docs)
- [ClawHub Bavlio skill page](https://clawhub.ai/bavlio/skills/bavlio)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with inline bash commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bavlio API key and explicit user approval before paid lead searches, enrichment, or campaign launch.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
