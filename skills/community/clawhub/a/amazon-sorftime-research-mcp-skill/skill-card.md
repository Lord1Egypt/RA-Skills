## Description:

Provides an /amazon-analyse workflow that uses Sorftime MCP data to analyze Amazon competitor listings across copy, reviews, keywords, market dynamics, and saves Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdabiao](https://clawhub.ai/user/liangdabiao)

### License/Terms of Use:

MIT

## Use Case:

External sellers, marketplace analysts, and ecommerce operators use this skill to collect Sorftime MCP data for an Amazon ASIN, assess competitor listing strategy, review sentiment, keywords, and market movement, and produce a structured competitive analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASINs, product queries, reviews, and derived competitive analysis may be sent to Sorftime.

Mitigation: Review the data being submitted before use and only run the workflow when sending that information to Sorftime is acceptable.

Risk: API keys may be exposed if stored directly in .mcp.json or embedded in command history.

Mitigation: Keep .mcp.json out of source control, prefer environment-variable or header-based secret handling when supported, and use a least-privilege API key.

Risk: The referenced Sorftime capability set includes mutable keyword-library tools and non-Amazon data sources beyond the core Amazon analysis workflow.

Mitigation: Avoid invoking TikTok, 1688, or keyword-library mutation tools unless those actions are explicitly needed and reviewed.

Risk: Generated reports are saved locally and may contain sensitive competitive analysis.

Mitigation: Store reports in an appropriate local directory, review contents before sharing, and archive or delete reports according to the user's data-retention needs.

## Reference(s):

- [Sorftime MCP API](references/sorftime-mcp-api.md)
- [Sorftime MCP Tool Reference](references/api-tools-reference.md)
- [Report Management](references/report-management.md)
- [Sorftime Website](https://www.sorftime.com)
- [ClawHub Skill Page](https://clawhub.ai/liangdabiao/skills/amazon-sorftime-research-mcp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save analysis reports under reports/ using filenames that include ASIN, marketplace, and date.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
