## Description:

Category Selection automates Amazon category market research with a five-dimension scoring model and produces Markdown, Excel, and HTML analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chanalii](https://clawhub.ai/user/chanalii)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, product researchers, and marketplace analysts use this skill to investigate Amazon categories, compare market opportunity signals, and generate actionable category-entry recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically uses a Sorftime API key and sends category or product queries to Sorftime.

Mitigation: Install only where Sorftime credential use and external category/product queries are approved, and keep API keys in controlled configuration.

Risk: Generated HTML, CSV, and Excel reports may contain third-party product data that can execute as browser script or spreadsheet formulas.

Mitigation: Treat generated reports as untrusted until HTML/script escaping, innerHTML rendering, and spreadsheet formula neutralization are reviewed or fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chanalii/skills/category-selection)
- [Scoring standard](artifact/references/scoring-standard.md)
- [API quick reference](artifact/references/api-quick-reference.md)
- [Category API reference](artifact/references/category-api-reference.md)
- [Sorftime MCP API reference](artifact/references/sorftime-mcp-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Excel workbooks, HTML dashboards, JSON/CSV data files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable Amazon site, category name or node ID, and Top N analysis limits.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
