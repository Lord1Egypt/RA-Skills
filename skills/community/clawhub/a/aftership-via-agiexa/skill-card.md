## Description:

Describes Agiexa's planned AfterShip integration for Shopify shipment tracking and return review, and explains the consent-based waitlist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devkrutik](https://clawhub.ai/user/devkrutik)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify merchants use it to understand the planned AfterShip integration, see how an agent could investigate delivery issues and returns, and optionally join Agiexa's launch waitlist with explicit consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AfterShip capabilities are preview-only and cannot be used for live shipment or return management today.

Mitigation: Treat the examples as previews and do not rely on the integration for live operations before it launches.

Risk: Waitlist signup shares the user's email and role with Agiexa; an optional URL may identify their store.

Mitigation: Obtain explicit consent, confirm the details with the user, and omit optional information they do not want to share.

Risk: Approving or rejecting a return cannot be undone in AfterShip.

Mitigation: Review the return details and obtain the user's explicit confirmation before making either decision.

## Reference(s):

- [AfterShip integration page](https://agiexa.com/integrations/aftership)
- [AfterShip tools](artifact/references/tools.md)
- [AfterShip use cases](artifact/references/use-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API calls]

**Output Format:** [Natural-language guidance and Markdown summaries; a JSON request may be prepared for the consent-based waitlist.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described AfterShip tools are preview-only until the planned November 2026 launch; waitlist submission requires explicit consent.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
