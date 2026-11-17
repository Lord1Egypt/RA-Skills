## Description:

Helps Digikala sellers search categories, create and assign products, and upload images through the marketplace API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ehsanghaffar](https://clawhub.ai/user/ehsanghaffar)

### License/Terms of Use:

MIT-0

## Use Case:

Digikala sellers and their agents use this skill to find and validate categories, prepare product listings, upload images, and assign products to a seller account. Orders, finance, and customer data workflows are outside its scope.

### Deployment Geography for Use:

Global (for Digikala marketplace sellers)

## Known Risks and Mitigations:

Risk: Product creation, assignment, title changes, and image uploads can change a live seller account.

Mitigation: Show the exact proposed change, obtain user approval, and review product details and images before execution.

Risk: A seller access token can expose business data or permit storefront changes if leaked.

Mitigation: Use the narrowest available token scopes; never paste tokens into chat, logs, or repositories, and revoke any exposed token.

Risk: A custom API host or local sandbox can receive a seller token.

Mitigation: Never use a real token with custom hosts or sandbox settings; use a throwaway token for local testing.

## Reference(s):

- [Digikala skill on ClawHub](https://clawhub.ai/ehsanghaffar/skills/digikala)
- [Digikala API endpoint reference](references/endpoints.md)
- [Digikala Marketplace Open API](https://seller.digikala.com/open-api/v1/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or change live product listings and upload images after user approval.]

## Skill Version(s):

0.1.5 (source: ClawHub server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
