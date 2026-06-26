## Description: <br>
ETF Investment Assistant queries ETF quotes, searches and compares ETFs, summarizes ETF categories, and estimates dollar-cost averaging outcomes for common China, Hong Kong, and overseas ETFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squally2k](https://clawhub.ai/user/squally2k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up ETF prices, find common ETF codes, compare two ETFs, review mainstream ETF categories, and estimate DCA outcomes. The results are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes local shell commands and makes Yahoo Finance network requests for quote and comparison commands. <br>
Mitigation: Review the shell script before installation and expect outbound requests to Yahoo Finance when using market-data commands. <br>
Risk: Investment tips, comparison output, and DCA calculations may be incomplete, simplified, or unsuitable for financial decisions. <br>
Mitigation: Treat all output as informational only and verify investment decisions with qualified financial sources. <br>
Risk: Input validation is basic for ETF codes, search terms, calculator amounts, and time horizons. <br>
Mitigation: Prefer numeric ETF codes and simple search terms, and review command inputs before execution. <br>


## Reference(s): <br>
- [Yahoo Finance chart data endpoint](https://query1.finance.yahoo.com/v8/finance/chart/${code}.SS) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quote and comparison commands make Yahoo Finance network requests; calculator and summary outputs are informational only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
