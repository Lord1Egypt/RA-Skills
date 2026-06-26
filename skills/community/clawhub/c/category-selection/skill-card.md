## Description: <br>
Category Selection helps agents run Amazon category research with Sorftime data, apply a five-dimension scoring model, and generate Markdown, Excel, and HTML market-analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChanaLii](https://clawhub.ai/user/ChanaLii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace operators, analysts, and agent users can use this skill to evaluate Amazon categories, compare market opportunity signals, and generate selection reports from Sorftime API data. It is intended for category analysis workflows where the user has authorized Sorftime API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Sorftime credentials from SORFTIME_API_KEY or .mcp.json and uses them in external API requests. <br>
Mitigation: Use a scoped or limited Sorftime key where possible, store it only in approved local configuration, and rotate it if it may have been exposed. <br>
Risk: Example requests place the API key in the request URL, which can expose credentials through copied commands, shell history, logs, or shared raw response files. <br>
Mitigation: Replace placeholder keys before use, avoid sharing command history or generated raw files, and review outputs and logs before distribution. <br>
Risk: Generated category reports may contain stale, incomplete, or misleading market data from external APIs. <br>
Mitigation: Treat generated recommendations as decision support and verify important figures against authoritative business data before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ChanaLii/category-selection) <br>
- [Sorftime MCP API Quick Reference](references/api-quick-reference.md) <br>
- [Category API Reference](references/category-api-reference.md) <br>
- [Five-Dimension Scoring Model Standard](references/scoring-standard.md) <br>
- [Sorftime MCP API Documentation](references/sorftime-mcp-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown reports, Excel workbooks, HTML dashboards, JSON data files, logs, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces category-reports output directories containing decoded Sorftime responses, scored category data, product lists, and generated report artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
