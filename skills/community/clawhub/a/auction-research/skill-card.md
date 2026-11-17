## Description:

Researches Bonhams auctions and lots through Crawlora, including sale calendars, estimates, and realized prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and other users can search Bonhams sales and lots, compare estimates and realized prices, and inspect auction details using a Crawlora API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and route parameters are sent to Crawlora under the user's API key.

Mitigation: Avoid secrets and private client information in queries; revoke or rotate the key when no longer needed.

## Reference(s):

- [Auction Research endpoint reference](artifact/reference/endpoints.md)
- [Auction Research on ClawHub](https://clawhub.ai/crawlora-org/skills/auction-research)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Bonhams auction and lot data; requires a Crawlora API key.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
