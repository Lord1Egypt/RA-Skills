## Description:

Collects Sorftime MCP data for Amazon ASINs, classifies keywords across eight advertising dimensions with an LLM-assisted workflow, and generates keyword research reports, CSV libraries, and HTML dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdabiao](https://clawhub.ai/user/liangdabiao)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, advertising operators, and ecommerce analysts use this skill to research ASIN keyword coverage, classify terms for campaign strategy, and produce reusable reports for PPC planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends ASIN, keyword, and product research data to Sorftime.

Mitigation: Use it only where that data sharing is approved, and avoid submitting confidential product or campaign data unless Sorftime handling is acceptable.

Risk: The skill depends on an API key stored in .mcp.json.

Mitigation: Keep .mcp.json in a trusted project location, verify the configured endpoint is the intended Sorftime URL, and protect or rotate the key if exposure is suspected.

Risk: Generated HTML and CSV reports may contain untrusted API or product-derived data.

Mitigation: Review and sanitize generated reports before opening or sharing them, especially CSV spreadsheet cells and HTML output, until escaping and spreadsheet-cell sanitization are confirmed.

Risk: Generated keyword reports are stored locally and may include business-sensitive research data.

Mitigation: Store output directories in access-controlled locations and remove or archive reports according to the team's data retention policy.

## Reference(s):

- [Sorftime MCP API Interface Documentation](artifact/references/sorftime-mcp-api.md)
- [Sorftime MCP Tool Reference](artifact/references/api-tools-reference.md)
- [Report Management](artifact/references/report-management.md)
- [Sorftime MCP Documentation](artifact/references/sorftime_mcp文档.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include Markdown, CSV, JSON, HTML, and plain-text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated local keyword-reports directories for a supplied ASIN and Amazon marketplace site.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
