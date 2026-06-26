## Description: <br>
Generates a Markdown metrics card for a single Chinese A-share stock, covering valuation, profitability, cash flow, debt, dividends, and trading activity for comparison and tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoiFG](https://clawhub.ai/user/JoiFG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate a repeatable, local Markdown research card for one A-share stock symbol. The card is intended for learning, comparison, and tracking of factual metrics, not for buy, sell, target-price, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The stock symbol is sent to public market-data services. <br>
Mitigation: Use only symbols intended for public lookup and avoid entering confidential identifiers or private research notes as parameters. <br>
Risk: The skill creates or replaces a local Markdown file. <br>
Mitigation: Keep the output path inside an intended notes folder and review the target path before running the skill. <br>
Risk: Public market data can be delayed, unavailable, rate-limited, or affected by upstream API changes. <br>
Mitigation: Check the card's source and timestamp notes, and verify important metrics against primary filings or trusted market-data sources before relying on them. <br>


## Reference(s): <br>
- [A Share Metrics Card on ClawHub](https://clawhub.ai/JoiFG/a-share-metrics-card) <br>
- [Eastmoney push2 quote endpoint](https://push2.eastmoney.com/api/qt/stock/get) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown file with metric sections, source notes, timestamps, and follow-up questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or replaces a local stock card at the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
