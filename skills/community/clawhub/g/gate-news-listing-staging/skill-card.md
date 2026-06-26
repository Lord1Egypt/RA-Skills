## Description: <br>
Exchange listing tracker for exchange listing, delisting, and maintenance announcements using read-only Gate News and Gate Info MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto market analysts use this skill to retrieve exchange listing, delisting, and maintenance announcements, then receive a structured activity report with optional coin fundamentals and market context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may be incomplete or stale if Gate News or Gate Info MCP tools are unavailable, delayed, or return partial public market data. <br>
Mitigation: Label missing data clearly, degrade to announcement-only output when enrichment fails, and verify important trading decisions against primary exchange announcements. <br>
Risk: Users may overinterpret listing reports as trading advice for volatile newly listed tokens. <br>
Mitigation: Keep language neutral, avoid buy or sell advice, include volatility and liquidity warnings, and state that the report is not investment advice. <br>
Risk: The skill depends on enabled MCP tools for public market data. <br>
Mitigation: Enable only trusted Gate News and Gate Info MCP tools documented by the skill before use. <br>


## Reference(s): <br>
- [Gate News Listing Runtime Rules](references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](references/info-news-runtime-rules.md) <br>
- [Gate News Listing MCP Specification](references/mcp.md) <br>
- [Gate News Listing Scenarios & Prompt Examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with tables and concise narrative summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public announcement, fundamentals, and market data returned by documented read-only MCP tools; includes missing-data labels and risk disclaimers.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter: 2026.4.6-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
