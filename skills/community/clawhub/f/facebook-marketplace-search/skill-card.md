## Description:

Search Facebook Marketplace listings near a specified location with filters for radius, price range, limit, and pickup-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexanderhe88](https://clawhub.ai/user/alexanderhe88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query a user-provided local Marketplace-compatible service for nearby Facebook Marketplace listings and receive normalized listing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper delegates Marketplace data access and authentication behavior to the local service configured by the user.

Mitigation: Only point MARKETPLACE_API_BASE_URL at a Marketplace service you control and trust.

Risk: Dependency hygiene issues can affect runtime integrity if packages are installed without review.

Mitigation: Install in a virtual environment and review or pin dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexanderhe88/skills/facebook-marketplace-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns normalized listing fields including id, title, price, location, seller_name, image_url, and listing_url; error responses are JSON.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
