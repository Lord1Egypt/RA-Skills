## Description:

Ecwid REST API v3 integration for managing e-commerce store data including products, orders, customers, categories, discount coupons, promotions, abandoned carts, and store profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droneitgroup](https://clawhub.ai/user/droneitgroup)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators, ecommerce teams, and developers use this skill to query Ecwid REST API v3 documentation and prepare HTTP requests for store profile, catalog, order, customer, coupon, promotion, and abandoned cart data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ecwid API tokens can expose sensitive store, order, and customer data if granted broad access or shared in logs and chats.

Mitigation: Use a read-only, least-privilege token, avoid exposing customer PII, and rotate the token if exposure is suspected.

Risk: Enabling write HTTP methods can mutate production store data.

Mitigation: Keep HTTP methods limited to GET unless store mutation is intentional and tested first in a sandbox or test store.

## Reference(s):

- [Ecwid REST API reference](https://docs.ecwid.com/api-reference)
- [Ecwid REST API authentication](https://docs.ecwid.com/api-reference/rest-api/authentication)
- [Publisher profile](https://clawhub.ai/user/droneitgroup)
- [Skill page](https://clawhub.ai/droneitgroup/skills/ecwid-ecommerce)
- [Publisher homepage](https://github.com/droneitgroup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP endpoint details and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ecwid REST API paths, query parameters, response field descriptions, scope guidance, and bearer-token setup instructions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
