## Description:

A-Share Multi-Dimensional Quantitative Analysis is a hosted MCP server that provides broker research reports, AI news analysis, and comprehensive stock analysis for China's A-share market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-evan](https://clawhub.ai/user/li-evan)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to connect to a hosted MCP service for researching Chinese A-share companies, reviewing broker reports and news analysis, and retrieving stock-level trading analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags an insecure remote MCP setup with hardcoded authentication and database credentials.

Mitigation: Review before installing or using; do not send API keys unless the service is served over HTTPS with a trusted hostname and the publisher confirms credential rotation, least-privilege database access, and scoped or revocable user tokens.

Risk: The security guidance says exposed default tokens and database credentials should be treated as compromised.

Mitigation: Require credential rotation before relying on the service, and verify that replacement credentials are scoped and revocable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li-evan/skills/a-share-multidim-quant-analysis)
- [Hosted MCP endpoint](http://42.121.167.42:9800/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted text returned by MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool outputs may include broker report text, news summaries, sentiment, investment recommendations, and stock analysis sections.]

## Skill Version(s):

1.4.0 (source: server release metadata; artifact frontmatter reports 1.3.0 and pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
