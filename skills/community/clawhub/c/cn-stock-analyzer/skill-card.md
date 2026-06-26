## Description: <br>
Trading Quant provides market data and quantitative analysis for A-shares, US stocks, Hong Kong stocks, precious metals, capital flows, market anomalies, and multi-factor stock scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch finance and news data, analyze stock and market conditions, compare capital flows, and generate informational trading-analysis summaries. Outputs should be treated as market-analysis assistance rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces market-analysis outputs that could be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational only and require users to make independent financial decisions. <br>
Risk: The skill contacts third-party finance and news services and may use local watchlist symbols when no ticker is supplied. <br>
Mitigation: Review configured symbols and network access before use, especially in sensitive environments. <br>
Risk: Market caches and snapshots are stored locally, so stale or local data may affect analysis. <br>
Mitigation: Check source labels and freshness indicators before relying on a result. <br>
Risk: Some sentiment scores may fall back to keyword-based methods rather than FinBERT. <br>
Mitigation: Use sentiment scores as directional context and verify important conclusions against source news. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/cn-stock-analyzer) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like command output with inline shell commands and market-analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include locally cached market snapshots, source labels, scores, risk flags, and data-freshness notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
