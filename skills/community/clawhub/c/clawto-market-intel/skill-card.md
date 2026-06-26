## Description: <br>
Aggregates public market sentiment, index quotes, market news, macro calendar items, and cryptocurrency technical-analysis signals for concise market briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawto](https://clawhub.ai/user/clawto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect concise public-market snapshots, including sentiment, index movements, headlines, macro events, and crypto technical indicators. Its outputs are informational market summaries and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market summaries and strategy-style notes may be mistaken for financial advice. <br>
Mitigation: Present outputs as informational only and require users to verify market decisions with independent sources or qualified advisors. <br>
Risk: The skill contacts public finance, news, and crypto data services, so outputs depend on third-party availability and freshness. <br>
Mitigation: Check source timestamps and retry or cross-check key data before relying on time-sensitive summaries. <br>
Risk: Broad market-related trigger phrases may activate the skill during ordinary finance discussions. <br>
Mitigation: Confirm user intent before running data-fetching scripts when a query is ambiguous. <br>


## Reference(s): <br>
- [Crypto Analysis Framework](references/crypto-analysis.md) <br>
- [Alternative.me Crypto Fear & Greed API](https://api.alternative.me/fng/?limit=1) <br>
- [CNN Fear & Greed Dataviz API](https://production.dataviz.cnn.io/index/fearandgreed/graphdata) <br>
- [CNBC Market News RSS](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114) <br>
- [MarketWatch Top Stories RSS](https://feeds.marketwatch.com/marketwatch/topstories) <br>
- [Eastmoney Quotes API](https://push2.eastmoney.com/api/qt/ulist.np/get) <br>
- [ClawHub Skill Page](https://clawhub.ai/clawto/clawto-market-intel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise market-summary text or Markdown, with shell commands used by the agent to fetch data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live public market data, RSS headlines, technical-indicator summaries, and strategy-style informational notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
