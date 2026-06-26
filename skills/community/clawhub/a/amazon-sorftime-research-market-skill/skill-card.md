## Description: <br>
Provides Sorftime-backed Amazon product research by collecting market, keyword, trend, competitor, and review data, then guiding an LLM agent through product attributes, cross-analysis, VOC, barriers, and selection decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace researchers, Amazon sellers, and agent operators use this skill to collect Sorftime market evidence and produce structured product opportunity analysis, including VOC themes, competitive barriers, go/no-go scoring, Markdown reports, JSON data, and an HTML dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sorftime receives submitted product keywords, ASINs, marketplace sites, and research parameters. <br>
Mitigation: Use the skill only when that data can be shared with Sorftime, and avoid submitting confidential product plans or sensitive internal research terms. <br>
Risk: The Sorftime API key may be exposed through screenshots, logs, shell history, shared reports, or local configuration files. <br>
Mitigation: Store the key outside shared artifacts, redact it before sharing output, and rotate it if it appears in logs or reports. <br>
Risk: Generated raw data files may retain market, review, and competitor research data after the analysis is complete. <br>
Mitigation: Review generated raw/ files before sharing the report directory and delete retained raw data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangdabiao/amazon-sorftime-research-market-skill) <br>
- [Sorftime MCP API quick reference](references/api-quick-reference.md) <br>
- [Sorftime API reference](references/api-reference.md) <br>
- [LLM prompt templates](references/prompt_templates.md) <br>
- [Sorftime MCP API documentation](references/sorftime-mcp-api.md) <br>
- [Product research troubleshooting guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data files, raw API response files, HTML dashboard output, shell commands, and agent guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a product-research report directory containing report.md, data.json, dashboard.html, and raw data files when run against a product keyword and marketplace site.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
