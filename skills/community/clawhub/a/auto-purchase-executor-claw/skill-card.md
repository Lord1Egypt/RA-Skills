## Description:

自动下单执行虾 is a rule-driven purchase automation skill that monitors inventory, price, and schedule triggers, creates supplier orders, and can execute payment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, operations, and engineering teams use this skill to configure automatic replenishment, price-triggered purchases, recurring renewals, and emergency supplier orders. Because it can initiate payment-capable actions, live use should require strong approval, credential, endpoint, idempotency, and stop controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real supplier orders and execute payment-capable workflows automatically.

Mitigation: Default to dry-run mode and require explicit human approval before any payment-capable action.

Risk: Continuous monitoring can keep executing purchases without a clear operational stop mechanism.

Mitigation: Provide a clear stop control and require idempotency checks before enabling monitoring.

Risk: Supplier endpoints and credentials may be too broadly trusted for live purchasing.

Mitigation: Validate supplier endpoints and use least-privilege credentials stored outside source files.

Risk: Dynamic expression and database handling can be unsafe for payment-capable automation.

Mitigation: Remove eval/source interpolation and parameterize database access before live use.

## Reference(s):

- [支付安全规范](references/payment-security.md)
- [采购规则引擎配置指南](references/purchase-rules.md)
- [供应商对接协议](references/supplier-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment-capable execution guidance and operational controls]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
