## Description: <br>
Handles Alipay payment service flows by parsing cashier links, submitting payment requests, and querying payment results when a user intends to pay with Alipay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to process Alipay cashier links, guide wallet authorization when needed, submit payment, and check payment status after the user indicates completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that broad payment language can start live Alipay payment and wallet workflows without a clear hard confirmation gate. <br>
Mitigation: Require explicit user confirmation that the merchant, amount, payment method, and Alipay cashier link are visible and correct before wallet authorization or payment submission. <br>
Risk: The skill installs and executes a payment CLI package. <br>
Mitigation: Verify the fixed npm package integrity for @alipay/agent-payment@1.0.0 and obtain user consent before installation or execution. <br>
Risk: Payment links, authorization links, and short URLs can expose live payment flow state if mishandled. <br>
Mitigation: Do not log, persist, truncate, rewrite, or send payment URLs outside the user-selected channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yun520-1/alipay-pay-for-service) <br>
- [Payment skills GitHub repository](https://github.com/alipay/payment-skills) <br>
- [Alipay agent-payment npm package](https://www.npmjs.com/package/@alipay/agent-payment) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text, shell commands, and structured JSON handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include complete Alipay cashier URLs, short payment-status URLs, and MEDIA image paths from CLI output.] <br>

## Skill Version(s): <br>
1.0.9-beta1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
