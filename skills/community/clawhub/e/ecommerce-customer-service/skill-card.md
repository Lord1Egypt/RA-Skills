## Description:

当用户需要回答商品咨询、整理售前 FAQ 或起草售后解释时，根据商品资料、买家问题和已确认店铺规则生成可复制回复及商家待核实事项；在线详情支持抖音和小红书，不会自动发送消息或办理售后。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

商家客服人员可根据已确认的商品资料和店铺规则起草买家回复、整理售前 FAQ 与售后说明，并单列需商家核实的事项。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned CLI package, including during credential login, and the security scan is incomplete because two references were unresolved.

Mitigation: Review and pin a CLI version before use, especially for credential setup; resolve the references and complete a security review before relying on the scan.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/ecommerce-customer-service)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese customer-reply drafts or FAQ content with separate merchant verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts only; does not send messages or perform order or after-sales actions.]

## Skill Version(s):

0.1.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
