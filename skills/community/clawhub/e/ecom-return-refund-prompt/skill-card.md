## Description: <br>
Standardized reusable prompt template for e-commerce customer service agents to handle buyer return, exchange, and refund inquiries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer service teams and e-commerce agents use this prompt template to generate policy-aware responses for buyer return, exchange, refund, and after-sale dispute inquiries based on supplied order and platform-policy inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect policy values or unsupported compensation promises could mislead buyers. <br>
Mitigation: Verify the platform return window, category rules, refund timelines, and compensation terms before using the generated response. <br>
Risk: Responses may include sensitive buyer or order information. <br>
Mitigation: Use only the necessary buyer and order fields, and review outputs to avoid exposing internal order details, seller addresses, or other buyers' information. <br>
Risk: High-value disputes, legal or safety concerns, or strongly negative buyer sentiment may require human judgment. <br>
Mitigation: Escalate those cases to a human support agent and use the prompt output only as draft guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/ecom-return-refund-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style customer service response text with greeting, status, operation guidance or alternative options, warm tips, and closing sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses buyer, order, issue, timing, category, platform-policy, and language placeholders; defaults output language to zh-CN when no language is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
