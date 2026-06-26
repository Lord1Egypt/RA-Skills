## Description: <br>
Analyzes Amazon competitor listings across copy strategy, reviews, keywords, and market dynamics, then saves a Markdown report to the reports directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChanaLii](https://clawhub.ai/user/ChanaLii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and ecommerce analysts use this skill to investigate a competitor Amazon ASIN, collect Sorftime MCP product data, and produce a structured competitive intelligence report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product research queries and an API key to Sorftime MCP. <br>
Mitigation: Install only when Sorftime is trusted for the relevant research data, and keep API keys out of generated reports and shared logs. <br>
Risk: Generated Markdown reports become persistent business records under reports/. <br>
Mitigation: Review reports for confidential product strategy, pricing, and market intelligence before sharing or committing them. <br>
Risk: The artifact references broader Sorftime APIs, including keyword-library actions not clearly needed for reporting. <br>
Mitigation: Restrict normal use to read-only Amazon analysis endpoints unless account-changing keyword-library actions are explicitly intended. <br>


## Reference(s): <br>
- [Amazon Analyse ClawHub Page](https://clawhub.ai/ChanaLii/amazon-analyse) <br>
- [Sorftime](https://www.sorftime.com) <br>
- [Sorftime MCP API](references/sorftime-mcp-api.md) <br>
- [API Tools Reference](references/api-tools-reference.md) <br>
- [Report Management](references/report-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves dated analysis reports under reports/ and may include decoded Sorftime MCP data summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
