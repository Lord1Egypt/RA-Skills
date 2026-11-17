## Description:

Helps agents publish GPS-anchored BillboardBug deals and social posts, then verify them with read-back receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgaut007](https://clawhub.ai/user/bgaut007)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators and their agents use this skill to create location-based promotions and social posts on BillboardBug, then check the published content and report a receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deals and chirps become public under the account holder's name.

Mitigation: Confirm the business, promotion, media, location, and caption with the account holder before publishing.

Risk: Public posts can disclose exact coordinates or deal identifiers.

Mitigation: Leave precise coordinates and deal identifiers out of public posts unless the account holder intends to share them.

Risk: Promotions may remain visible after their intended end date.

Mitigation: Record the end date and disable the deal when the promotion ends.

Risk: An exposed API key could let others act under the account holder's identity.

Mitigation: Keep the key out of chat, posts, logs, and command arguments; use a private header file for requests.

## Reference(s):

- [BillboardBug API documentation](https://east-us-api.billboardbug.com/public-api/docs)
- [BillboardBug OpenAPI specification](https://east-us-api.billboardbug.com/public-api/spec)
- [BillboardBug homepage](https://billboardbug.com)
- [BillboardBug ClawHub release](https://clawhub.ai/bgaut007/skills/billboardbug)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance, API request examples, and read-back receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided BillboardBug API key and explicit confirmation before publishing.]

## Skill Version(s):

1.2.3 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
