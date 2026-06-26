## Description: <br>
Ecwid Ecommerce documents Ecwid REST API v3 workflows for store data including products, orders, customers, categories, discount coupons, promotions, abandoned carts, and store profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droneitgroup](https://clawhub.ai/user/droneitgroup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and store operators use this skill to let an agent query Ecwid store data and prepare API requests for catalog, order, customer, promotion, cart, coupon, and profile workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ecwid order, customer, and cart queries can expose customer personal data such as email addresses, phone numbers, billing or shipping addresses, tracking numbers, and private admin notes. <br>
Mitigation: Use responseFields to limit returned data and redact customer personal data before sharing outputs. <br>
Risk: A broad Ecwid secret token or enabled write methods can give an agent more store access than intended. <br>
Mitigation: Use a read-only token with the smallest required scopes where possible, keep HTTP methods to GET for read-only use, and avoid full admin tokens unless write access is intentional. <br>


## Reference(s): <br>
- [Ecwid API Reference](https://docs.ecwid.com/api-reference) <br>
- [Ecwid API Authentication](https://docs.ecwid.com/api-reference/rest-api/authentication) <br>
- [Publisher Homepage](https://github.com/droneitgroup) <br>
- [Ecwid Ecommerce ClawHub Release](https://clawhub.ai/droneitgroup/ecwid-ecommerce) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples, curl commands, and API parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include guidance for limiting Ecwid API responses with responseFields and for handling JSON API responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
