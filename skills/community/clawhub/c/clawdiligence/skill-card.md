## Description:

AI M&A due diligence analyst that analyzes companies, values businesses, parses Japanese financial statements, and generates acquisition simulation reports from public filings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yu010101](https://clawhub.ai/user/yu010101)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and M&A practitioners use this skill to collect or parse Japanese public filing data, structure financial statements, calculate valuation metrics, and produce buyer-oriented acquisition simulation reports. It can optionally export structured balance sheet, profit-and-loss, and valuation data to Excel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces valuation and acquisition guidance that could be mistaken for professional financial advice.

Mitigation: Present outputs as AI-generated analysis from public information, retain the investment-advice disclaimer, and require professional review before decisions.

Risk: EDINET_API_KEY may appear in logs on request failures unless errors are sanitized.

Mitigation: Run in a controlled workspace, avoid exposing unrelated environment variables, and review or sanitize error output before sharing logs.

Risk: Public filing extraction and comparable-company assumptions may be incomplete or stale.

Mitigation: Require source annotations for numerical values, mark unsupported figures as unknown or unverified, and review comparable multiples before relying on the report.

Risk: Dependency behavior can change over time and affect reproducibility.

Mitigation: Pin or review the Python dependencies httpx, pdfplumber, and openpyxl when reproducible operation matters.

## Reference(s):

- [Account Mapping Reference](references/account-mapping.md)
- [Valuation Guide](references/valuation-guide.md)
- [EDINET Disclosure Download](https://disclosure2dl.edinet-fsa.go.jp)
- [Kanpou Official Gazette](https://kanpou.npb.go.jp)
- [EDINET API](https://api.edinet-fsa.go.jp/api/v2)
- [ClawHub Skill Page](https://clawhub.ai/yu010101/skills/clawdiligence)
- [Publisher Profile](https://clawhub.ai/user/yu010101)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown analysis report with structured financial tables, source annotations, optional JSON inputs to helper scripts, shell commands, and optional Excel workbook output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses EDINET_API_KEY for automated EDINET retrieval when available; falls back to user-provided text or PDF input.]

## Skill Version(s):

0.1.1 (source: server release metadata and artifact/plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
