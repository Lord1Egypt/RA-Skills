## Description:

Analyzes how financial events historically affected related assets by identifying similar events, inferring cross-market relationships, and producing Chinese reports and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to examine historical reactions to financial shocks such as oil moves, gold rallies, rate hikes, VIX spikes, and currency strength. It supports event-driven analysis across assets and economies, then assembles Chinese-language reports with data-backed charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance can expose API tokens if users echo TUSHARE_TOKEN or store secrets directly in shell startup files.

Mitigation: Use a protected secret mechanism and presence-only environment checks; do not print tokens or place raw credentials in ~/.bashrc.

Risk: The workflow sends financial data requests to Yahoo Finance, Tushare, and optionally FRED.

Mitigation: Review the required data sources and credentials before installation, and run the skill only where that network access is acceptable.

Risk: Font installation guidance may use privileged system package commands.

Mitigation: Prefer an isolated environment with locked Python dependencies, and use sudo package installation only when intentionally administering the host.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laigen/skills/financial-event-impact-analyzer)
- [Indicator Mapping Reference](artifact/references/indicator_mapping.md)
- [Chinese Report Template](artifact/references/report_template.md)
- [Tushare Registration](https://tushare.pro/register)
- [FRED API Key Documentation](https://fred.stlouisfed.org/docs/api/api_key.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown reports with PNG charts and JSON/CSV data artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis outputs under ~/.openclaw/workspace/memory/reports/<analysis_folder>/ and uses Yahoo Finance, Tushare, and optionally FRED as data sources.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact/skill.json lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
