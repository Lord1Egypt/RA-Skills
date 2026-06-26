## Description: <br>
Collects Amazon keyword data with the Sorftime MCP API, classifies keywords into eight advertising strategy categories with optional LLM support, and generates Markdown, CSV, and HTML research outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers, PPC operators, and ecommerce analysts use this skill to research an ASIN's keyword landscape, classify terms by advertising use, and produce local reports for campaign planning and market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASINs, product details, keyword research data, and generated classification prompts may contain sensitive business research. <br>
Mitigation: Run only when sharing that data with Sorftime and the selected LLM provider is acceptable, and restrict access to generated report directories. <br>
Risk: The Sorftime API key is read from local MCP configuration and could be exposed through careless logging or copied URLs. <br>
Mitigation: Protect .mcp.json, avoid pasting or storing full Sorftime URLs that include the key, and rotate credentials if exposed. <br>
Risk: LLM or rule-based keyword classification can misclassify advertising terms and affect PPC decisions. <br>
Mitigation: Review negative, brand, core, and other high-impact categories before importing results into advertising workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangdabiao/amazon-sorftime-research-keywords-skill) <br>
- [Sorftime MCP API reference](references/sorftime-mcp-api.md) <br>
- [Sorftime MCP tools reference](references/api-tools-reference.md) <br>
- [Report management](references/report-management.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, CSV, HTML, JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, structured CSV keyword libraries, JSON summaries, text word lists, and HTML dashboards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local keyword-reports directories for the requested ASIN and Amazon site; optional product information can improve classification quality.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
