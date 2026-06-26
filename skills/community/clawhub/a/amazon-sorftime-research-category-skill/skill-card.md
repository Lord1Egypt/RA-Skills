## Description: <br>
Analyzes Amazon product categories with Sorftime data and a five-dimension scoring model, then generates market research reports for category selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External sellers, ecommerce analysts, and developers use this skill to research Amazon categories, compare market opportunity signals, and produce category selection reports from Sorftime data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local Sorftime API credential may be read automatically and sent in URL-based API requests. <br>
Mitigation: Review the skill before installation, use a dedicated low-privilege Sorftime key, prefer an environment variable over storing keys in .mcp.json, and rotate the key if it is exposed. <br>
Risk: Category queries, business research targets, generated logs, and raw response files may contain sensitive commercial context. <br>
Mitigation: Avoid submitting sensitive research targets unless Sorftime sharing is acceptable, and do not share generated logs or raw response files outside the intended workspace. <br>
Risk: The generated dashboard has an external ECharts CDN dependency. <br>
Mitigation: Open the dashboard only when that external dependency is acceptable, or replace it with an approved internal or pinned copy before wider use. <br>


## Reference(s): <br>
- [Sorftime MCP API Quick Reference](references/api-quick-reference.md) <br>
- [Category API Reference](references/category-api-reference.md) <br>
- [Five-Dimension Scoring Model Standard](references/scoring-standard.md) <br>
- [Sorftime MCP API Documentation](references/sorftime-mcp-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, Excel workbooks, HTML dashboards, JSON data files, CSV exports, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default workflow analyzes Top 20 products and can be configured for larger category samples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
