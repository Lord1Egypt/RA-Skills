## Description: <br>
Automates quarterly financial report generation with dividend-adjusted total return calculations for stock performance reports, quarterly earnings summaries, and return analytics using CSV price data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to analyze stock CSV exports and generate quarterly reports with price returns, dividend-adjusted total returns, dividends, high and low prices, and volume metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial return calculations can be incorrect or misapplied if CSV inputs are incomplete, malformed, or use unexpected column semantics. <br>
Mitigation: Run the skill only on CSV files you intend to analyze and independently verify financial calculations before investment or business decisions. <br>
Risk: The analyzer depends on local Python and pandas availability and expected CSV columns for date, price, and volume data. <br>
Mitigation: Confirm pandas is installed and validate input files against the documented CSV format before relying on generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/financial-report-automator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; analyzer results are Python dictionaries or JSON-like reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes local stock CSV files, requires Python 3.10+ and pandas, and produces local financial report data without hidden network or credential behavior.] <br>

## Skill Version(s): <br>
1.2.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
