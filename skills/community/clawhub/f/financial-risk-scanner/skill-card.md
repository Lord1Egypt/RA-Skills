## Description:

Scans listed company financial statements for potential fraud risks, accounting anomalies, audit concerns, and governance red flags using 21 financial risk indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, investors, and developers use this skill to review Chinese A-share listed companies for financial statement red flags and produce a structured risk assessment report. The output supports follow-up review and cross-validation against filings, annual reports, and company announcements.

### Deployment Geography for Use:

Global, with analysis scope limited to Chinese A-share listed companies.

## Known Risks and Mitigations:

Risk: Dependency versions are not pinned to exact releases.

Mitigation: Install in a dedicated virtual environment and pin approved versions of tushare, pandas, and their transitive dependencies before operational use.

Risk: Generated report filenames may include unsanitized company names.

Mitigation: Use the explicit output path option or sanitize report filenames before running in shared or sensitive workspaces.

Risk: Missing financial data can lead some checks to score as no risk.

Mitigation: Review data completeness warnings and validate generated conclusions against annual reports, regulatory filings, and company announcements.

Risk: The Tushare API token is required for financial data access.

Mitigation: Use a dedicated token limited to this workflow and avoid exposing it outside the runtime environment.

## Reference(s):

- [Risk Indicators Reference](references/risk_indicators.md)
- [Tushare API Field Mapping Reference](references/api_reference.md)
- [Tushare Pro](https://tushare.pro)
- [ClawHub Skill Page](https://clawhub.ai/laigen/skills/financial-risk-scanner)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report files with terminal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a single Tushare stock code and TUSHARE_TOKEN; the default report path is ~/.openclaw/workspace/memory/financial-risk/.]

## Skill Version(s):

1.0.4 (source: server release and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
