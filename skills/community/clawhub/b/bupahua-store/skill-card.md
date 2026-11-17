## Description:

Bupahua Store searches the 不怕花 shopping catalog by keyword and returns matching products with prices, stock status, and product links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[285984303](https://clawhub.ai/user/285984303)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and agents assisting them use this skill to search the 不怕花 catalog for products, prices, stock status, and product detail links. It is intended for product lookup, not order support, after-sales service, or cross-platform price comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad shopping questions may trigger this skill and send product keywords to the 不怕花 service.

Mitigation: Install it only when generic shopping questions should search the 不怕花 catalog, and disclose or account for product keywords being sent to that service.

Risk: The skill depends on a dedicated store API key.

Mitigation: Protect the API key as a secret, avoid sharing it in prompts or logs, and rotate it if exposure is suspected.

Risk: Displayed original-price comparisons may be misleading because the security guidance identifies a price-formatting bug.

Mitigation: Fix and verify price formatting before relying on original-price comparisons in user-facing responses.

Risk: The skill calls an external API endpoint for catalog search.

Mitigation: Pin or allowlist the expected API endpoint before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/285984303/skills/bupahua-store)
- [不怕花 website](https://bupahua.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-formatted shopping search results, with optional JSON when the script is called with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product names, prices, stock status, and bupahua.com product links when available.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
