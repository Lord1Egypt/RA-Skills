## Description:

粤收付交易集成：用于聚合支付、托管支付、checkout-js、下单、查单、关单、退款、对账、支付通知、签名验签、请求头、幂等、交易终态、本地沙箱和支付上线；不用于企业/个人商户进件、图片上传、商户业务开通、商户详情或申请状态查询，这些任务使用 huifu-merchant-onboarding。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanglin88](https://clawhub.ai/user/huanglin88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical operators, and merchant integration teams use this skill for Yue Shou Fu payment API integration guidance, code examples, troubleshooting, compliance checks, and best practices across PHP, Java, Python, Go, and Node.js. It focuses on transaction workflows such as order creation, payment queries, refunds, reconciliation, notifications, signatures, idempotency, sandbox testing, transfers, cashout, and profit sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated transfer, cashout, refund, and profit-sharing code can affect real funds if used without review.

Mitigation: Test in a sandbox, require human review before production use, and verify amounts and destination accounts.

Risk: Payment callbacks and final states can be misread, leading to duplicate or incorrect transaction handling.

Mitigation: Use signed callbacks, idempotent processing, and query-based final-state confirmation.

Risk: Merchant private keys and signing material are sensitive.

Mitigation: Protect private keys and validate signing and verification behavior before deployment.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/huanglin88/payment-expert/tree/main/skills/cnyepay)
- [ClawHub skill page](https://clawhub.ai/huanglin88/skills/cnyepay)
- [Yue Shou Fu API documentation](https://open.cnyepay.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; generated payment integration code and operational guidance require review before production use.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
