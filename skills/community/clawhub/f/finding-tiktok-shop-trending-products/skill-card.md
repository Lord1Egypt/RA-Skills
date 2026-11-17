## Description:

Finds trending TikTok Shop products using Apify's apidojo TikTok scraper and reports creator promotion density, engagement signals, price range, and trend momentum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External TikTok Shop sellers, affiliates, dropshippers, and e-commerce trend researchers use this skill to identify products gaining viral commerce momentum and decide which items merit deeper sourcing or promotion review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented REST fallback places the Apify API token in a query string, which is riskier than needed.

Mitigation: Prefer the Apify MCP server or a helper that sends the token in an Authorization header, use a least-privilege Apify token, monitor usage costs, and avoid the documented REST fallback as written.

Risk: Product extraction, trend stage, and pricing signals can be incomplete or misleading when captions are ambiguous, product variants differ, or suspicious pricing appears.

Mitigation: Verify product identity, shop links, pricing, creator activity, and sourcing legitimacy before acting on the trend report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-tiktok-shop-trending-products)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with product tables, scoring notes, and optional CSV or JSON actor results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports product names, creator counts, views, engagement rate, trend stage, score, and saturation or pricing alerts when supported by collected data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
