## Description:

Search products across Taobao, Tmall, JD, PDD, 1688, AliExpress, Douyin, and XHS with no API keys required for product lookup, supplier search, and price comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoyuji12138](https://clawhub.ai/user/gaoyuji12138)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and sourcing teams use this skill to search Chinese e-commerce marketplaces, parse product URLs, retrieve product details, and compare prices or suppliers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill runs an unpinned third-party npm MCP package whose reviewed code is not included.

Mitigation: Run the MCP server in a restricted environment and prefer a pinned reviewed package version.

Risk: Shopping-search queries or product URLs may contain confidential procurement information.

Mitigation: Avoid confidential procurement searches or internal-only product URLs unless approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoyuji12138/skills/gaoyuji)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown or structured text with product search results, product details, parsed product identifiers, and MCP setup configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required by default; SHOPME_API_BASE can override the API endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; skill frontmatter metadata lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
