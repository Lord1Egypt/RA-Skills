## Description: <br>
微信支付委托代扣接入解决方案，覆盖周期扣款 / 先享后付场景下的纯签约、支付中签约、申请扣款、预扣费通知、解约、查询、退款、对账全链路，提供选型、示例代码、业务速查、质量评估和排障能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and troubleshoot WeChat Pay delegated deduction integrations for merchant and service-provider payment flows. It helps route questions across product selection, sample request/response material, signing and callback rules, quality checks, refunds, reconciliation, and issue diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment integration examples may become outdated or diverge from current WeChat Pay requirements. <br>
Mitigation: Verify implementation details against current official WeChat Pay documentation before production use. <br>
Risk: Incorrect callback handling could accept forged, replayed, or mismatched payment events. <br>
Mitigation: Use HTTPS callback endpoints, validate signatures and amounts, and apply idempotency and reconciliation checks. <br>
Risk: Secrets or certificates could be exposed if users paste production credentials into chat. <br>
Mitigation: Do not provide API keys, private keys, certificates, or other production secrets to the agent. <br>


## Reference(s): <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Merchant product selection guide](artifact/references/1-商户/产品选型/产品介绍.md) <br>
- [Merchant signing and verification rules](artifact/references/1-商户/接入指南/签名与验签规则.md) <br>
- [Merchant callback handling](artifact/references/1-商户/接入指南/回调处理.md) <br>
- [Merchant quality checklist](artifact/references/1-商户/接入指南/接入质量检查.md) <br>
- [Service-provider product selection guide](artifact/references/2-服务商/产品选型/产品介绍.md) <br>
- [Service-provider signing and verification rules](artifact/references/2-服务商/接入指南/签名与验签规则.md) <br>
- [Service-provider callback handling](artifact/references/2-服务商/接入指南/回调处理.md) <br>
- [Service-provider quality checklist](artifact/references/2-服务商/接入指南/接入质量检查.md) <br>
- [WeChat Pay delegated deduction product introduction](https://pay.weixin.qq.com/doc/v2/merchant/4011986647.md) <br>
- [WeChat Pay delegated deduction onboarding process](https://pay.weixin.qq.com/doc/v2/merchant/4011986709.md) <br>
- [WeChat Pay periodic deduction documentation](https://pay.weixin.qq.com/doc/v2/merchant/4011986682.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with selected official request, response, callback, checklist, and troubleshooting excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is documentation-only and instructs the agent to ask for integration mode and scenario details before providing payment-flow guidance.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
