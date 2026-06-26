## Description: <br>
AI M&A due diligence analyst that analyzes companies, values businesses, parses Japanese financial statements, and generates acquisition simulation reports from public filings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yu010101](https://clawhub.ai/user/yu010101) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to perform M&A due diligence workflows for Japanese companies, including public filing collection, financial statement extraction, valuation, risk review, and acquisition report generation. The skill is especially oriented toward EDINET, Kanpo, uploaded PDFs, and user-provided financial data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic EDINET retrieval and report generation can create local files or overwrite existing outputs if paths are chosen carelessly. <br>
Mitigation: Set EDINET_API_KEY only when automatic EDINET downloads are intended, and choose output directories deliberately before running fetch, parse, or export commands. <br>
Risk: Financial conclusions may be misleading when filings are incomplete, PDF extraction fails, or figures cannot be traced to a source. <br>
Mitigation: Require source citations for figures, mark unavailable values as unknown or unverified, and keep the generated report's investment-advice disclaimer. <br>
Risk: Image-based PDFs may not yield reliable text for downstream financial parsing. <br>
Mitigation: Ask for OCR-processed text or an extractable PDF before continuing with valuation steps. <br>


## Reference(s): <br>
- [Account Mapping Reference](references/account-mapping.md) <br>
- [Valuation Guide](references/valuation-guide.md) <br>
- [EDINET Disclosure System](https://disclosure2dl.edinet-fsa.go.jp) <br>
- [EDINET API](https://api.edinet-fsa.go.jp/api/v2) <br>
- [Kanpo](https://kanpou.npb.go.jp) <br>
- [ClawHub Skill Page](https://clawhub.ai/yu010101/clawdiligence) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown due diligence reports with financial tables, JSON-structured financial data, shell commands, and optional Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use EDINET_API_KEY for automatic EDINET downloads and may write local text or .xlsx report files when requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
