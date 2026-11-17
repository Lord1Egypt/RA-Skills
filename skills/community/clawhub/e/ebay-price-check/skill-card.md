## Description:

Search eBay for current and sold item prices, then summarize price ranges, averages, shipping context, and condition-based results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kl0nlutiy](https://clawhub.ai/user/kl0nlutiy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent to check eBay listings for an item, compare active and sold-price ranges, and get a concise pricing summary before buying, selling, or researching resale value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to eBay and may reveal sensitive item interests or business context.

Mitigation: Use non-sensitive, non-confidential search terms and avoid personal or proprietary identifiers.

Risk: Price summaries may be incomplete or unavailable because eBay can limit search frequency and sold data is not available for all items.

Mitigation: Treat summaries as a quick estimate and verify important pricing decisions against current eBay listings.

Risk: The bundled wrapper path and Python stdout handling may cause reliability failures in some environments.

Mitigation: Validate the command locally before relying on it, and invoke or patch the Python script directly if the wrapper fails.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown-style text summary with item counts and price statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on eBay availability, page structure, and rate limits.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
