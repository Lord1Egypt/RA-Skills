## Description:

Amazon Analyse analyzes Amazon competitor listings with Sorftime data, covering listing copy, reviews, keywords, market trends, and strategy recommendations, then produces a Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chanalii](https://clawhub.ai/user/chanalii)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, brand teams, and developers use this skill to analyze a competitor ASIN across supported Amazon marketplaces and generate a structured competitive intelligence report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ASINs, keywords, and related analysis inputs to Sorftime.

Mitigation: Install only when sharing those inputs with Sorftime is acceptable, and avoid including sensitive product plans in prompts or API arguments.

Risk: The artifact shows API keys in command URLs and .mcp.json examples.

Mitigation: Use a scoped, revocable API key and avoid placing real keys directly in shell history, command lines, or committed configuration files.

Risk: The security summary notes broader account-changing keyword tools than the stated analysis task needs.

Mitigation: Do not permit keyword collection changes unless explicitly requested, and verify the exact add, move, or remove action before execution.

## Reference(s):

- [API Tools Reference](references/api-tools-reference.md)
- [Report Management](references/report-management.md)
- [Sorftime MCP API](references/sorftime-mcp-api.md)
- [Sorftime MCP Documentation](references/sorftime_mcp文档.txt)
- [Sorftime](https://www.sorftime.com)
- [Sorftime MCP Endpoint](https://mcp.sorftime.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves reports as reports/analysis_{ASIN}_{site}_{date}.md and may use Sorftime MCP data, including up to 100 reviews.]

## Skill Version(s):

1.0.0 (source: server release metadata and auto changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
