## Description: <br>
Exchange listing tracker for listing, delisting, and maintenance announcements using Gate News and Gate Info MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve exchange listing, delisting, and maintenance announcements, then receive a structured activity report enriched with public coin and market context where available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Gate News and Gate Info MCP tools, so missing or failing tools can leave announcement or enrichment data incomplete. <br>
Mitigation: Confirm MCP availability before use, degrade gracefully on individual tool failures, and clearly label unavailable data. <br>
Risk: Exchange listing and newly listed coin reports can be mistaken for trading recommendations. <br>
Mitigation: Keep the report neutral, include the non-investment-advice disclaimer, and surface volatility and liquidity warnings for new listings. <br>
Risk: Future listing plans or rumors may be requested but are not supported by the announcement feed. <br>
Mitigation: Use only published announcements, do not predict listings, and distinguish confirmed announcements from unavailable data. <br>


## Reference(s): <br>
- [Gate News Listing Runtime Rules](artifact/references/gate-runtime-rules.md) <br>
- [Info & News Common Runtime Rules](artifact/references/info-news-runtime-rules.md) <br>
- [Gate News Listing MCP Specification](artifact/references/mcp.md) <br>
- [Gate News Listing Scenarios](artifact/references/scenarios.md) <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-news-listing) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Analysis, Guidance] <br>
**Output Format:** [Markdown report with tables, summaries, and risk warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only MCP announcement, coin information, and market snapshot data; unavailable data is labeled rather than fabricated.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter version 2026.4.6-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
