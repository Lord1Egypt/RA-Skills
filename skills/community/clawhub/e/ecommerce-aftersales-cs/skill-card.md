## Description:

电商售后客服规范应答生成。当客服人员需要处理退换货申请、物流异常咨询、售后补偿协商三类高频售后诉求时调用，确保应答话术统一符合品牌服务规范。

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support teams use this skill to draft standardized Chinese aftersales replies for return or exchange requests, logistics exceptions, and compensation negotiations. The generated responses help agents keep wording empathetic, policy-bound, privacy-aware, and consistent with brand service rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated aftersales replies may overstate refund eligibility, compensation authority, logistics status, or policy commitments if staff do not verify the case details.

Mitigation: Require staff review against current order status, policy limits, refund eligibility, and compensation authority before sending any generated customer reply.

Risk: Customer replies may include sensitive personal details if source messages contain full phone numbers, addresses, or similar data.

Mitigation: Follow the skill's masking rule and redact private data with *** before sending responses.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese customer-service response drafts with structured steps and policy-aware wording]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; staff should verify order status, policy limits, refund eligibility, and compensation authority before sending generated replies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
