## Description: <br>
Provides a paid product-introduction workflow for Alipay AI Pay and Agent Wallet using an HTTP 402 payment handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill when they want an introduction to Alipay AI Pay or Agent Wallet. The skill requests the product resource, handles direct responses or payment-required responses, and hands the complete 402 response to the related payment skill when payment is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead the user into a paid-resource workflow before product details are shown. <br>
Mitigation: Use it only when the user asks for Alipay AI Pay or Agent Wallet product information, and make the payment-required state clear before handing off to the payment skill. <br>
Risk: Changing signed URLs or HTTP 402 response details can break the payment handoff. <br>
Mitigation: Preserve signed URLs, response headers, and response body content exactly when passing the payment response to the related skill. <br>


## Reference(s): <br>
- [Alipay payment skills](https://github.com/alipay/payment-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and HTTP response handling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exact signed URLs, response headers, or payment-response content that should be preserved during payment handoff.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
