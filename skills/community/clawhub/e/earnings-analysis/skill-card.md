## Description: <br>
Analyzes company earnings reports when requested or when a stock is mentioned with earnings-related terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzy11650](https://clawhub.ai/user/dzy11650) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, investors, and agent users can request a concise earnings analysis for a stock ticker. The skill gathers recent revenue, profit, margin, cash-flow, forecast-surprise, rating, valuation, and earnings-calendar signals and returns analytical observations without explicit buy or sell advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved earnings reports and IMA notes may reveal sensitive ticker, portfolio, or watchlist activity. <br>
Mitigation: Install only if local report and note persistence is acceptable, and review or delete saved reports and notes when the analyzed tickers are sensitive. <br>
Risk: Generated financial analysis can be incomplete or misleading if source data is stale, unavailable, or interpreted incorrectly. <br>
Mitigation: Review the generated Markdown and underlying financial data before relying on the analysis; treat the output as analytical signal labeling, not buy or sell advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dzy11650/earnings-analysis) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown earnings analysis report saved as a local .md file, with important results copied into IMA notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-stock reports are limited to 600 characters; batch analyses are limited to 300 characters per stock; the skill avoids explicit buy or sell recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
