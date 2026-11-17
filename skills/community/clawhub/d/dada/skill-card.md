## Description:

Dada is a same-city delivery guide for platform selection, merchant integration, delivery API workflows, order lifecycle handling, fee estimation, callbacks, and shipping constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and merchants use this skill to understand Dada same-city delivery scenarios, compare delivery options, and plan API integration for order creation, status queries, cancellations, fee estimates, callback handling, merchant registration, and shop setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends recording all API request and response logs, which can expose customer names, phone numbers, addresses, coordinates, callback URLs, signatures, and secrets.

Mitigation: Log only allowlisted operational fields, redact personal data and credentials, restrict log access, and use short retention for delivery API logs.

## Reference(s):

- [Dada Open Platform production API](https://newopen.imdada.cn)
- [Dada Open Platform test API](https://newopen.qa.imdada.cn)
- [Dada add order endpoint](https://newopen.imdada.cn/api/order/addOrder)
- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/dada)
- [ClawHub publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, API Calls, Configuration]

**Output Format:** [Markdown with API examples and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include delivery API request examples, callback handling guidance, order status mappings, and integration recommendations.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
