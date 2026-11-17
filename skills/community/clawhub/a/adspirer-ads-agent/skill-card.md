## Description:

AI agent that manages ad campaigns across Google Ads, Meta Ads, LinkedIn Ads, and TikTok Ads, including campaign creation, live performance analysis, keyword research, and budget optimization through natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amekala](https://clawhub.ai/user/amekala)

### License/Terms of Use:

MIT

## Use Case:

External marketers, PPC specialists, agencies, and e-commerce teams use this skill to read campaign performance, research keywords, create paused campaigns, optimize budgets, and manage cross-platform advertising workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, pause, resume, and optimize campaigns on real ad accounts, which can affect advertising spend.

Mitigation: Require explicit user confirmation for write or spend-affecting actions, and keep newly created campaigns paused for user review before spend begins.

Risk: The release delegates high-impact ad-account control to an unpinned external plugin.

Mitigation: Review the Adspirer plugin, OAuth scopes, and connected ad accounts before installing or authorizing access.

Risk: Scheduled monitors, reports, or research tasks may continue running after setup.

Mitigation: Review active scheduled tasks and monitors regularly, and disable any automation that is no longer needed.

## Reference(s):

- [Adspirer homepage](https://www.adspirer.com)
- [Adspirer ad account connections](https://adspirer.ai/connections)
- [Adspirer MCP server source](https://github.com/amekala/ads-mcp)
- [ClawHub skill page](https://clawhub.ai/amekala/skills/adspirer-ads-agent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, markdown, configuration]

**Output Format:** [Markdown with tool names, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose and perform read-only analysis, and can request confirmation before spend-affecting write actions through the Adspirer plugin.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
