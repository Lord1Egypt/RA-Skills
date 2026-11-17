## Description:

Queries Ozon product traffic keywords through the Clawec API, including search index, conversion, supply-demand ratio, natural traffic keywords, and advertising traffic keywords for keyword research, competitor analysis, SEO, and ad selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to retrieve Ozon keyword metrics for product traffic analysis, keyword discovery, SEO planning, and advertising selection. It helps compare keyword types, search demand, conversion signals, supply-demand ratio, and competitor counts for up to 10 product IDs per request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Ozon product IDs, keyword filters, and authenticated API requests to ClawEC.

Mitigation: Use the skill only when sharing this product research data with ClawEC is acceptable, and review ClawEC data handling before using sensitive business inputs.

Risk: API credentials may be exposed through hardcoded values, shared logs, or command history.

Mitigation: Store CLAWEC_API_KEY as a secret environment variable and avoid sharing logs that include commands, headers, or authorization values.

## Reference(s):

- [Ozon Product Traffic Keyword Response Schema](references/response-schema.md)
- [Clawec API Base URL](https://www.clawec.com/api)
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/skills/clawec-ozon-product-traffic-keywords)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional JSON API response details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report language is Chinese; API access requires CLAWEC_API_KEY and sends Ozon product IDs and keyword filters to ClawEC.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
