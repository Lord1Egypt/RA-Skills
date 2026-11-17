## Description:

AliMerce 商城助手 supports e-commerce customer service, sales assistance, product management, and order handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alimerce](https://clawhub.ai/user/alimerce)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-facing commerce agents use this skill to answer product questions, retrieve order information, recommend products, assist with checkout, and manage customer preferences when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad user, account, and customer preference tools can expose or change sensitive commerce data without sufficient boundaries.

Mitigation: Use backend-enforced authorization, tenant and object scoping, least-privilege API tokens, and audit logging for all tool access.

Risk: Customer contact details and preferences may be stored or updated without clear consent.

Mitigation: Require clear customer consent before writing preferences or contact details, and limit stored data to the current commerce use case.

Risk: High-risk actions such as product deletion, shipment or delivery status changes, and administrator role changes can materially affect the store.

Mitigation: Enforce explicit approval or denial rules for product_delete, order_update to shipped or delivered, and user_update role changes.

## Reference(s):

- [AliMerce skill page](https://clawhub.ai/alimerce/skills/alimerce)
- [Skill definition](artifact/SKILL.md)
- [AliMerce MCP tools](artifact/alimerce-mcp.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Natural-language responses with structured tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [High-risk product, order, and role changes require approval before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
