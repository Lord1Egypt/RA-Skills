## Description:

A Chinese-language workflow for researching convertible bonds by screening bond candidates, analyzing bond terms and event probabilities, extending into underlying-equity and industry research, and producing investment research summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackluson](https://clawhub.ai/user/jackluson)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to structure convertible-bond research, including market screening, single-bond analysis, downward-revision and forced-redemption event assessment, underlying-equity analysis, industry comparison, valuation, and final investment research summaries. The skill is research support and does not replace independent financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on anchor-data.cn for convertible-bond market data and requires storing an Anchor Data API key in WorkBuddy MCP configuration.

Mitigation: Install only when use of anchor-data.cn is intended, keep the API key scoped and protected, and review WorkBuddy MCP configuration before enabling the connector.

Risk: Bond queries and related parameters may be sent to the external market-data service.

Mitigation: Avoid submitting confidential watchlists or sensitive investment strategy details unless that external data flow is acceptable.

Risk: Generated investment summaries may be incomplete, stale, or misleading if market data, web search results, or key variables are not independently checked.

Mitigation: Treat reports as research support, verify source data and assumptions, preserve risk disclosures, and do not treat outputs as financial advice.

## Reference(s):

- [Source repository](https://github.com/jackluson/convertible-bond-research)
- [ClawHub skill page](https://clawhub.ai/jackluson/skills/convertible-bond-research)
- [Anchor Data](https://www.anchor-data.cn)
- [Anchor Data MCP introduction](https://www.anchor-data.cn/blog/anchor-mcp-intro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or HTML-formatted research reports with configuration snippets and tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use anchor-bond MCP data, westock-data, and web search; generated reports should be treated as research support rather than financial advice.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
