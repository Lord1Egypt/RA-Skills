## Description:

Searches Channel3 product data for products, prices, availability, merchant offers, and buy links across retailers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanfen-c3](https://clawhub.ai/user/evanfen-c3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to find products, compare prices and availability, and return concise recommendations with merchant links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product search terms, filters, and image URLs are sent to Channel3 using the configured API key.

Mitigation: Avoid sensitive purchase intents and private image URLs; review requests before running searches.

Risk: Returned buy links may use affiliate-tracked redirects.

Mitigation: Verify merchant destinations and disclose or review affiliate redirects where required.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/evanfen-c3/skills/channel3-product-discovery)
- [Channel3 API docs](https://docs.trychannel3.com)
- [Channel3 website](https://trychannel3.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured text from the search script, typically summarized into Markdown lists or comparison tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHANNEL3_API_KEY, curl, and jq; sends product queries, filters, and image URLs to Channel3.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact/skill.yaml lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
