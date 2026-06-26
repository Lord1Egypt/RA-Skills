## Description: <br>
Integrate Chinese payment methods (WeChat Pay, Alipay, UnionPay) into applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft Chinese payment integrations for WeChat Pay, Alipay, and UnionPay, including payment creation, callbacks, refunds, reconciliation, amount conversion, and compliance checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment callback examples are under-scoped enough to risk unsafe order-state changes if copied into production. <br>
Mitigation: Review and harden callbacks before production use by adding full provider signature validation, replay checks, merchant, app, order, and amount validation, atomic idempotent state transitions, and fulfillment only on the first valid payment transition. <br>
Risk: The skill requires sensitive merchant credentials and can influence purchase, refund, and wallet-related workflows. <br>
Mitigation: Store payment credentials only in secret managers or environment variables, restrict refund and settlement permissions, test in provider sandboxes, and require review before connecting generated code to live payment accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/china-payment-integration) <br>
- [WeChat Pay merchant platform](https://pay.weixin.qq.com) <br>
- [Alipay open platform](https://open.alipay.com) <br>
- [WeChat Pay sandbox documentation](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=23_1) <br>
- [Alipay sandbox documentation](https://open.alipay.com/develop/sandbox/app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment provider setup steps, callback handling examples, refund snippets, and compliance checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
