## Description: <br>
AliMerce 商城 AI 助手技能 - 客服、销售、商品管理、订单处理 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alimerce](https://clawhub.ai/user/alimerce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customer-service and ecommerce operators use this skill to answer product questions, check orders, recommend products, assist checkout, and maintain customer preferences across Chinese, English, and Mongolian interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect products, orders, users, and customer-preference data through connected AliMerce tools. <br>
Mitigation: Install only against trusted AliMerce MCP/API servers, enforce server-side permissions, and use least-privilege API tokens. <br>
Risk: Business-impacting product, order, and user changes may occur without fully defined safeguards. <br>
Mitigation: Require human approval for product deletion, shipped or delivered order updates, administrator role changes, and other material store changes. <br>
Risk: Customer preferences and contact details may include personal data. <br>
Mitigation: Collect clear customer consent and define retention and deletion rules before storing or updating customer memory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alimerce/alimerce) <br>
- [AliMerce MCP Tools](artifact/alimerce-mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown and structured tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes customer-facing response patterns and high-risk operation approval guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
