## Description:

Research iOS App Store apps with the AppHitlist MCP server. Use when the user asks which new apps already make money, what earns the most in a category, which apps are climbing or entering the daily App Store charts, how much an app makes, how long an app's Meta ads have run, or what users complain about in an app or category. Covers niche discovery, competitor analysis, ad research and complaint-based opportunity finding. Needs the AppHitlist MCP server connected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmdincer](https://clawhub.ai/user/mmdincer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use AppHitlist to research iOS app markets, competitors, chart movement, advertising activity, and user complaints through its MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AppHitlist revenue and download figures are model estimates and may not reflect audited results.

Mitigation: Label figures as AppHitlist estimates, retain free-access ranges as ranges, and avoid presenting estimates as audited facts.

Risk: Connecting to the MCP server requires a private API key.

Mitigation: Keep the key in the MCP client's secret configuration; do not request it in chat or write it into generated files.

## Reference(s):

- [AppHitlist MCP API](https://apphitlist.com/api/mcp)

## Skill Output:

**Output Type(s):** [API calls, Analysis, Guidance, Markdown]

**Output Format:** [Natural-language research summaries and AppHitlist MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [iOS App Store coverage; revenue and download figures are AppHitlist model estimates, reported as ranges on free access and monthly figures on Pro access.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
