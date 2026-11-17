## Description:

Helps agents implement Chinese authentication flows for WeChat and Alipay login, phone SMS verification, real-name verification, unified auth interfaces, session management, and compliance considerations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide implementation of authentication for China-facing applications, including OAuth login, SMS verification, real-name checks, account linking, and session handling.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Authentication examples may be copied as production code despite weak or incomplete controls.

Mitigation: Treat outputs as integration guidance and require security review before deployment.

Risk: SMS verification can be abused or bypassed if OTPs and attempts are handled weakly.

Mitigation: Use cryptographic OTP generation, enforced rate limits and attempt counters, short TTLs, and atomic one-time verification.

Risk: OAuth and identity verification flows can expose accounts or sensitive identity data if validation and privacy controls are incomplete.

Mitigation: Validate OAuth state, keep platform secrets server-side, encrypt identity data, obtain required consent, and perform provider-specific review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/china-auth-integration)
- [WeChat QR Connect endpoint](https://open.weixin.qq.com/connect/qrconnect)
- [WeChat OAuth access token endpoint](https://api.weixin.qq.com/sns/oauth2/access_token)
- [WeChat Mini Program session endpoint](https://api.weixin.qq.com/sns/jscode2session)
- [Alibaba Cloud SMS endpoint](https://dysmsapi.aliyuncs.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with JavaScript examples, API flow steps, tables, and security rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth2 flow outlines, SMS provider examples, real-name verification notes, and security and compliance reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
