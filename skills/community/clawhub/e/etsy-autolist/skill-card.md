## Description:

Auto-create and manage digital product listings on Etsy using Etsy Open API v3, including listing creation, tagging, pricing, and draft publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and operators use this skill to configure Etsy API credentials and create draft digital-product listings in an Etsy shop. Reviewers should inspect the predefined listing data before use because the packaged script creates those specific drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script requires Etsy credentials and an OAuth access token with write access to a shop.

Mitigation: Use only an Etsy account where API write access is acceptable, store credentials as secrets, and revoke the token if the skill is no longer needed.

Risk: The packaged script creates hardcoded draft listings rather than deriving listing content from the user's product files.

Mitigation: Inspect and edit the LISTINGS data before execution, then review every draft in the Etsy dashboard before publishing.

Risk: The documented OAuth helper is not included in the artifact, so setup is incomplete as packaged.

Mitigation: Confirm a trusted OAuth flow is available before use and do not manually paste tokens into unreviewed code or logs.

## Reference(s):

- [Etsy Developer Portal](https://developer.etsy.com)
- [Etsy Open API Documentation](https://developer.etsy.com/documentation/)
- [Etsy Open API v3 Base URL](https://api.etsy.com/v3)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Text]

**Output Format:** [Markdown guidance with inline shell commands and Python script console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Etsy listings as drafts through authenticated Etsy API calls.]

## Skill Version(s):

1.0.17 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
