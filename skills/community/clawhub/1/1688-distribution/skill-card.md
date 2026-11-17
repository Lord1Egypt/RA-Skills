## Description:

Provides a single entry point for 1688 distribution workflows, including product selection and listing, order management, knowledge-base lookup, and shop binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce operators use this skill to manage 1688 distribution tasks through an agent, including selecting products, confirming shops, distributing listings, querying orders, sending seller follow-up messages, and retrieving 1688 distribution guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and use a 1688 Access Key for account-specific operations.

Mitigation: Install only from a trusted publisher, review credential storage behavior before use, and avoid sharing or exposing the Access Key.

Risk: The skill can query account, shop, and order data.

Mitigation: Use it only in workspaces where access to 1688 account and order information is appropriate.

Risk: The skill can perform distribution actions and send seller messages.

Mitigation: Require explicit confirmation before browser authorization, credential reset or clear actions, product distribution, and outbound seller messaging.

Risk: The security scan advises review of AK storage/status leakage and callback server binding/authentication before use.

Mitigation: Review or fix those areas before deploying the skill in production or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-distribution)
- [1688 authentication portal](https://clawhub.1688.com/)
- [Product selection reference](scripts/biz/product_search_helper/reference.md)
- [Offer information reference](scripts/biz/offer_info/reference.md)
- [Distribution execution reference](scripts/biz/distribute_helper/reference.md)
- [Shop information reference](scripts/biz/shop_info/reference.md)
- [Order management reference](scripts/biz/order_helper/reference.md)
- [Knowledge-base query reference](scripts/biz/knowledge_helper/reference.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, API Calls, Guidance]

**Output Format:** [JSON responses containing markdown, with shell command invocations for local CLI tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and uses 1688 Access Key authorization for account-specific operations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
