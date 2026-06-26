## Description: <br>
Generates A-share weekly financial research reports from public AKShare, Sina Finance, and Eastmoney data, including technical analysis, trading signals, risk assessment, charts, and PDF output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mli-cj](https://clawhub.ai/user/mli-cj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent operators use this skill to generate local weekly research-style reports for selected A-share stock codes. It supports market overview, technical indicators, signal summaries, risk scoring, charts, and report generation for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public financial-data network requests and may return delayed or incomplete market data. <br>
Mitigation: Use explicit stock-code invocations, verify important data against trusted sources, and review generated reports before relying on or sharing them. <br>
Risk: Generated trading signals, risk scores, stop-loss levels, and position suggestions can be mistaken for investment advice. <br>
Mitigation: Treat reports as informational analysis only and require qualified human review before making financial decisions. <br>
Risk: Local PDF generation depends on Python packages and rendering dependencies such as WeasyPrint. <br>
Mitigation: Install dependencies from vetted sources and keep rendering packages updated or pinned to patched versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mli-cj/finance-research-report) <br>
- [Publisher profile](https://clawhub.ai/user/mli-cj) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Analysis, Shell commands] <br>
**Output Format:** [Local PDF report with generated Markdown-style financial analysis and chart images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires stock code arguments; generated reports are saved under output/ and should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
