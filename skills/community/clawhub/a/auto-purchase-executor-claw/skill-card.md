## Description: <br>
自动下单执行虾 is a rule-driven purchasing automation skill that monitors inventory, prices, renewal schedules, and supplier conditions to generate orders, execute payments, and archive notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, finance, and operations teams use this skill to configure rule-based replenishment, price-triggered purchases, renewals, and urgent supplier orders with budget checks, notifications, and audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate live supplier orders and payments. <br>
Mitigation: Require mandatory approval gates, dry-run validation, hard spending caps, and least-privilege test credentials before connecting real procurement or payment accounts. <br>
Risk: A persistent monitoring daemon could continue making purchasing decisions after deployment. <br>
Mitigation: Define and test a stop or kill-switch workflow, monitoring alerts, and operator ownership before enabling daemon mode. <br>
Risk: Rule handling and budget checks may be unsafe without review. <br>
Mitigation: Review rule parsing, remove eval-based budget checks, and test duplicate-order and spending-limit controls before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/auto-purchase-executor-claw) <br>
- [支付安全规范](references/payment-security.md) <br>
- [采购规则引擎配置指南](references/purchase-rules.md) <br>
- [供应商对接协议](references/supplier-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce purchase-rule configuration, supplier API payloads, monitoring commands, and operational checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
