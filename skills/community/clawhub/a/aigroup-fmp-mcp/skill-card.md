## Description:

Use `aigroup-fmp-mcp` for listed-equity data from Financial Modeling Prep, including quotes, company profiles, statements, ratios, sector context, and calendar requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route public-company market-data requests through the Financial Modeling Prep MCP server for quotes, profiles, statements, ratios, market breadth, estimates, technical indicators, and calendar context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data outputs may be mistaken for investment advice.

Mitigation: Treat responses as financial information, not investment advice, and verify material decisions against authoritative sources.

Risk: Quotes, calendars, charts, and filings can be stale or date-sensitive.

Mitigation: Confirm and state quote, chart, statement, and calendar dates in user-facing answers.

Risk: The external Financial Modeling Prep MCP server may require its own account or API key outside this skill.

Mitigation: Configure and manage external server credentials according to the provider's terms before using the skill.

## Reference(s):

- [FMP MCP Capabilities](artifact/references/capabilities.md)
- [ClawHub Skill Page](https://clawhub.ai/jackdark425/skills/aigroup-fmp-mcp)
- [Project Homepage](https://github.com/jackdark425/aigroup-fmp-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text responses grounded in MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state relevant quote, chart, statement, and calendar dates clearly.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
