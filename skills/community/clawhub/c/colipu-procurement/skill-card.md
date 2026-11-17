## Description:

A ClawHub skill that helps agents search, place, query, and cancel Colipu B2B office-supply orders through Colipu APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simsq](https://clawhub.ai/user/simsq)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, procurement users, and agents use this skill to buy office supplies on Colipu, including product search, multi-SKU order submission, order lookup, order details, and cancellation. The skill is scoped to Colipu procurement workflows and excludes after-sales returns, contract negotiation, and non-Colipu purchasing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some shipped paths can place business orders without the final per-order confirmation promised by the skill.

Mitigation: Avoid colipu_order.py, colipu_search.place_order(), and quick_order() until they enforce a final confirmation step immediately before order confirmation.

Risk: The skill uses Colipu credentials and session cookies tied to purchasing authority.

Mitigation: Use a Colipu account with limited purchasing authority, keep credentials in environment variables or a secrets manager, and apply external quantity and budget limits.

Risk: Order, address, credential, cookie, request, and response data can contain sensitive business information.

Mitigation: Do not log or share passwords, cookies, full request bodies, full responses, addresses, or order details unless they are redacted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simsq/skills/colipu-procurement)
- [Colipu API reference](artifact/references/api.md)
- [Configuration guide](artifact/CONFIG.md)
- [Colipu H5 API host](https://h5vip.colipu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus script-generated console text and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated API calls that search products, pre-submit orders, confirm orders, poll order creation, query order details, and cancel eligible orders.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
