## Description: <br>
Analyze energy, metals, and agricultural commodity markets alongside macro indicators to generate cross-asset macro signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to fetch commodity market data, derive macro signals, and summarize inflation, growth, sector, and asset-class implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Finskills API key and may send requested commodity symbols or series to Finskills. <br>
Mitigation: Use it only where Finskills API use is approved, keep FINSKILLS_API_KEY secret, and avoid submitting sensitive portfolio, client, or proprietary trading information. <br>
Risk: Generated commodity and macro signals may be incomplete, stale, or misleading if treated as financial advice. <br>
Mitigation: Treat reports as informational analysis, verify market data and assumptions independently, and apply qualified review before investment or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/commodity-macro-signal) <br>
- [Project homepage](https://github.com/finskills/commodity-macro-signal) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills API key registration](https://finskills.net/register) <br>
- [Finskills commodity prices endpoint](https://finskills.net/v1/free/commodity/prices) <br>
- [Finskills commodity history endpoint](https://finskills.net/v1/free/commodity/history/{symbol}) <br>
- [Finskills FRED commodity endpoint](https://finskills.net/v1/free/commodity/fred/{seriesId}) <br>
- [Finskills IMF commodity endpoint](https://finskills.net/v1/free/commodity/imf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with commodity tables, ratios, macro synthesis, and sector implications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and uses Finskills commodity, FRED, and IMF endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
