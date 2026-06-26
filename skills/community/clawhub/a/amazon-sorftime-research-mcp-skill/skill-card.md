## Description: <br>
Analyzes Amazon competitor listings with Sorftime MCP data and produces Markdown reports covering listing copy, reviews, keywords, market trends, and strategy recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amazon marketplace operators, brand teams, and ecommerce analysts use this skill to collect Sorftime MCP data for a target ASIN and generate a structured competitor intelligence report. The report supports listing optimization, keyword strategy, pricing review, product positioning, and market monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Amazon product research data to Sorftime MCP and requires a Sorftime API key. <br>
Mitigation: Install only if you trust Sorftime, protect the API key, and avoid committing .mcp.json or other files containing credentials. <br>
Risk: Bundled references describe Sorftime tools that can change keyword collections or access non-Amazon research surfaces beyond the main analysis workflow. <br>
Mitigation: Allow only the Sorftime tools needed for the intended Amazon ASIN analysis unless the user explicitly approves broader tool use. <br>
Risk: The security verdict is suspicious because the bundled references expose unrelated account-changing tools and weak API-key handling. <br>
Mitigation: Review the security summary and guidance before deployment, then constrain agent permissions and outbound data according to the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangdabiao/amazon-sorftime-research-mcp-skill) <br>
- [Sorftime website](https://www.sorftime.com) <br>
- [Sorftime MCP endpoint](https://mcp.sorftime.com) <br>
- [API tools reference](references/api-tools-reference.md) <br>
- [Report management](references/report-management.md) <br>
- [Sorftime MCP API](references/sorftime-mcp-api.md) <br>
- [Sorftime MCP documentation](references/sorftime_mcp文档.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis reports as dated Markdown files under reports/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
