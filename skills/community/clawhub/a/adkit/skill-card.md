## Description:

Manage advertising campaigns across Meta, Google, TikTok, LinkedIn, Microsoft, Reddit, X, and Pinterest through the AdKit CLI or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeannen](https://clawhub.ai/user/jeannen)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and campaign operators use this skill to create, manage, and review paid advertising campaigns across supported platforms through AdKit CLI or MCP. It is intended for campaign execution; strategy and copywriting requests should use the linked strategy resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command phrases that overlap with built-in commands could cause confusion in some setups.

Mitigation: Confirm that AdKit MCP tools or the AdKit CLI are available, then use the documented AdKit interface for campaign operations.

Risk: Publishing a campaign can start paid advertising on connected accounts.

Mitigation: Keep creations in draft mode, review the drafts, and publish only after explicit user approval.

## Reference(s):

- [AdKit website](https://adkit.so)
- [AdKit MCP guide](artifact/mcp.md)
- [AdKit CLI guide](artifact/cli.md)
- [Meta Ads MCP](https://adkit.so/features/ads-mcp/meta)
- [Google Ads MCP](https://adkit.so/features/ads-mcp/google)
- [TikTok Ads MCP](https://adkit.so/features/ads-mcp/tiktok)
- [LinkedIn Ads MCP](https://adkit.so/features/ads-mcp/linkedin)
- [Microsoft Ads MCP](https://adkit.so/features/ads-mcp/microsoft)
- [Reddit Ads MCP](https://adkit.so/features/ads-mcp/reddit)
- [X Ads MCP](https://adkit.so/features/ads-mcp/x)
- [Pinterest Ads MCP](https://adkit.so/features/ads-mcp/pinterest)
- [AdKit strategy skills](https://github.com/adkit-so/skills)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, Guidance, Text summaries]

**Output Format:** [Ad platform operations through MCP or CLI, with campaign drafts and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Campaign creation defaults to drafts; publishing requires explicit user approval.]

## Skill Version(s):

0.2.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
