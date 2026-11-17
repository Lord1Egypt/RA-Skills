## Description:

Standardized reusable prompt template for e-commerce customer service agents to handle buyer return, exchange, and refund inquiries with friendly, policy-compliant responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support agents and e-commerce operators use this prompt to draft Chinese-language return, exchange, and refund replies based on order context, platform return window, product category, and escalation triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Buyer-provided text could steer the generated response away from the intended return and refund workflow.

Mitigation: Treat buyer text as untrusted data, validate structured fields such as issue_type and days_since_delivery, and isolate free-text reasons from operational instructions.

Risk: Generated replies could promise refunds, compensation, timelines, or legal interpretations that the platform has not authorized.

Mitigation: Validate outputs against the stated platform policy and keep human approval for refunds, compensation, legal, safety, or high-value disputes.

Risk: Customer-service replies may expose private order, seller, or third-party information if sensitive data is inserted into the prompt.

Mitigation: Limit prompt inputs to the minimum required fields and review replies before sending to ensure internal order details, seller addresses, and other buyers' information are not disclosed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured customer-service response text or Markdown sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output language is zh-CN unless the language input is set explicitly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
