## Description: <br>
Analyze listed company financials to detect 21 fraud risk indicators with severity ratings and cross-validation for accounting anomalies and governance issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, auditors, compliance reviewers, and developers use this skill to scan Chinese A-share listed companies for accounting anomalies, fraud-risk indicators, audit concerns, and governance red flags. It supports preliminary risk triage and report generation, not final investment, audit, or compliance decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Tushare API token is required to fetch financial data. <br>
Mitigation: Provide the token through the TUSHARE_TOKEN environment variable, keep it out of source control and chat transcripts, and run the skill in a Python virtual environment. <br>
Risk: Generated financial-risk reports are saved locally and may contain sensitive company analysis. <br>
Mitigation: Restrict access to the report directory and delete reports from ~/.openclaw/workspace/memory/financial-risk when they are no longer needed. <br>
Risk: Automated risk indicators can be incomplete, stale, or misleading without human review. <br>
Mitigation: Validate findings against original filings, company announcements, audit reports, and qualified financial judgment before making investment, audit, or compliance decisions. <br>


## Reference(s): <br>
- [Risk Indicators Reference](references/risk_indicators.md) <br>
- [Tushare API Field Mapping Reference](references/api_reference.md) <br>
- [Tushare Pro API](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown risk report with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves generated reports locally under ~/.openclaw/workspace/memory/financial-risk unless an explicit output path is supplied.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
