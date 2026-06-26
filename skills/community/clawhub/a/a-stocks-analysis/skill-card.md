## Description: <br>
A Stocks Analysis helps agents query and analyze read-only Chinese A-share and Hong Kong stock market data across market prices, fundamentals, indices, and related text sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roamer-remote](https://clawhub.ai/user/roamer-remote) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language stock research questions into read-only data lookups and structured market analysis. It is intended for research support and explicitly does not place trades, promise returns, or provide financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TAX_API_KEY for the external data provider. <br>
Mitigation: Configure the key only through the agent platform or environment and do not paste it into chat. <br>
Risk: Stock data and analysis may be mistaken for financial advice or trading recommendations. <br>
Mitigation: Use outputs only as research support, keep the no-investment-advice framing, and avoid trade execution or promised-return conclusions. <br>
Risk: The skill depends on an external provider at tax.yyyou.top. <br>
Mitigation: Confirm the provider is trusted before installation and treat provider outages or stale data as limits on confidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/roamer-remote/a-stocks-analysis) <br>
- [Data Provider Homepage](https://tax.yyyou.top/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown text with structured analysis, suggested HTTP GET calls, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAX_API_KEY for provider access; outputs are research support and not financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
