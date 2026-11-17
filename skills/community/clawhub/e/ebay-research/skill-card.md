## Description:

Researches eBay listings, items, and sellers through the Crawlora API and returns normalized JSON without scraping eBay pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Buyers, sellers, and researchers use this skill to compare eBay listings, inspect item details, and review seller profiles, feedback, and shops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, item IDs, seller names, and the API key are sent to Crawlora.

Mitigation: Use the skill only when third-party transmission is acceptable; keep private customer, business, and account-sensitive information out of queries.

## Reference(s):

- [eBay endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/ebay-research)
- [Crawlora API key and service](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listing and seller results may require pagination; API access requires a Crawlora key.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
