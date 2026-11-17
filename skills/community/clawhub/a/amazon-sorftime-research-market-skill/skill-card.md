## Description:

Performs interactive Amazon product-market research using Sorftime MCP data collection and LLM-guided analysis, producing Markdown reports, structured data, and dashboard views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdabiao](https://clawhub.ai/user/liangdabiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sellers, and market researchers use this skill to investigate Amazon product categories with Sorftime data, competitor review analysis, opportunity scoring, and product-entry recommendations. It supports a two-phase workflow: scripted data collection followed by interactive LLM analysis and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sorftime API credentials may be exposed through curl examples, shell history, logs, or local configuration.

Mitigation: Use a low-privilege Sorftime API key, avoid pasting real keys into commands, avoid logging secrets, and rotate any key exposed in logs or shell history.

Risk: Generated dashboard.html files can include third-party or LLM-derived content.

Mitigation: Open generated dashboards carefully, review dashboard content before sharing, and avoid treating generated findings as verified facts without source checks.

Risk: The workflow writes generated reports and raw API responses under product-research-reports.

Mitigation: Run the skill only in a project directory where these outputs are acceptable, and review generated files before committing or publishing them.

## Reference(s):

- [Product Research README](README.md)
- [Sorftime MCP API Quick Reference](references/api-quick-reference.md)
- [Sorftime API Reference](references/api-reference.md)
- [Sorftime MCP API Documentation](references/sorftime-mcp-api.md)
- [LLM Prompt Templates](references/prompt_templates.md)
- [Product Research Troubleshooting Guide](references/troubleshooting.md)
- [Sorftime MCP](https://sorftime.com/zh-cn/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON data files, and generated HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces report.md, data.json, dashboard.html, and raw API response files under product-research-reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
