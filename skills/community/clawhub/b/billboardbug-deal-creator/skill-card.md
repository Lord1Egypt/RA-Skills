## Description:

Helps agents publish location-based BillboardBug deals and social posts under an authorized account, then verify them by reading them back.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgaut007](https://clawhub.ai/user/bgaut007)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and their authorized agents use this skill to create map-anchored promotions and social posts on BillboardBug, confirm the published content, and record receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deals and posts are published publicly under the user's account.

Mitigation: Confirm the business, location, offer, media, and end date with the account holder before publishing.

Risk: The account API key could be exposed during publishing.

Mitigation: Keep the key in the environment and out of chat, posts, logs, and command-line arguments.

Risk: An incorrect update or deletion could affect an existing public deal or post.

Mitigation: Read back the target and require confirmation of its exact ID before changing or deleting it.

Risk: A promotion could remain active past its intended end date because the deal has no end-date field.

Mitigation: Record the end date and disable the deal when it expires.

## Reference(s):

- [BillboardBug API documentation](https://east-us-api.billboardbug.com/public-api/docs)
- [BillboardBug OpenAPI specification](https://east-us-api.billboardbug.com/public-api/spec)
- [BillboardBug homepage](https://billboardbug.com)
- [ClawHub skill release](https://clawhub.ai/bgaut007/skills/billboardbug-deal-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Markdown guidance and receipts with API commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing requires an account API key and explicit approval before creation.]

## Skill Version(s):

1.1.3 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
