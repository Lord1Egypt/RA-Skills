## Description:

Automates Amazon category research using Sorftime data and a five-dimension scoring model to produce market analysis reports for product selection decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdabiao](https://clawhub.ai/user/liangdabiao)

### License/Terms of Use:


## Use Case:

Developers, analysts, and Amazon sellers use this skill to collect Sorftime category data, score market opportunity, competition, barriers, and margin signals, and generate category selection reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can automatically use a local Sorftime API key and send it in request URLs.

Mitigation: Use a dedicated low-privilege Sorftime API key and avoid placing unrelated secrets in the .mcp.json available to this skill.

Risk: The security evidence says generated HTML reports may be unsafe when built from external data and currently depend on a CDN.

Mitigation: Review generated dashboard.html files before opening or sharing them, and fix HTML escaping and external dependency handling before broad use.

Risk: The security evidence verdict is suspicious and recommends review before installing.

Mitigation: Review and scan the skill before deployment, with particular attention to API key handling, external data rendering, and generated reports.

## Reference(s):

- [Five-Dimension Scoring Model Standard](artifact/references/scoring-standard.md)
- [Sorftime MCP API Quick Reference](artifact/references/api-quick-reference.md)
- [Sorftime MCP API Documentation](artifact/references/sorftime-mcp-api.md)
- [Category Selection API Reference](artifact/references/category-api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/liangdabiao/skills/amazon-sorftime-research-category-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Excel reports, HTML dashboards, command examples, and analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Sorftime category, keyword, trend, and product data; default analysis depth is Top 20 products unless configured otherwise.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
