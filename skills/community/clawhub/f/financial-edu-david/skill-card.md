## Description: <br>
Financial Edu David helps agents analyze A-share listed companies by collecting annual reports, extracting financial statements, calculating indicators, creating HTML dashboards, and cross-checking results against public financial data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidyin1976](https://clawhub.ai/user/davidyin1976) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and education-focused agents use this skill to guide A-share financial analysis workflows for a specified company over a recent multi-year period. It supports annual-report download, PDF table extraction, financial metric calculation, dashboard generation, and public-data cross-checking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Chinese financial-data websites and downloads annual-report PDFs. <br>
Mitigation: Run it in a dedicated project directory with expected network access, and review downloaded files and source URLs before using the results. <br>
Risk: PDF table extraction can miss or misread financial line items because annual-report layouts vary. <br>
Mitigation: Cross-check generated financial data against Eastmoney F10 or another trusted public data source before relying on the analysis. <br>
Risk: Generated dashboards and financial conclusions may be incomplete or misleading if source data is stale, unavailable, or parsed incorrectly. <br>
Mitigation: Treat outputs as analysis aids, verify important figures manually, and avoid using the generated content as sole financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidyin1976/skills/financial-edu-david) <br>
- [CNINFO API Reference](references/cninfo_api.md) <br>
- [Eastmoney F10 Data Interface](references/eastmoney_api.md) <br>
- [Financial Metrics Guide](references/metrics_guide.md) <br>
- [CNINFO announcement query](https://www.cninfo.com.cn/new/hisAnnouncement/query) <br>
- [Eastmoney F10 data endpoint](https://datacenter-web.eastmoney.com/api/data/v1/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, Python scripts, and generated PDF, XLSX, JSON, and HTML analysis artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact public Chinese financial-data websites and write generated reports, spreadsheets, JSON data, and dashboards to a user-provided directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
