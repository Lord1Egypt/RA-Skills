## Description:

动环综合网管（温湿度监控平台）交互式登录工具，自动识别图片验证码、使用 RSA-OAEP-SHA256 加密密码、触发短信验证码下发，并保存登录 Cookie 供脚本或定时任务复用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[antarctic-penguin971](https://clawhub.ai/user/antarctic-penguin971)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to complete an interactive login flow for an internal 动环 monitoring platform, including captcha handling, SMS 2FA triggering, and cookie persistence for automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles passwords and session cookies in ways that could expose them.

Mitigation: Use only in a private trusted environment with a dedicated account, protect generated password and cookie files, restrict cookie file permissions, and clean temporary files after use.

Risk: The login script disables TLS certificate verification for curl requests.

Mitigation: Fix TLS verification before using real credentials, or limit use to a trusted internal network where the certificate and endpoint have been independently validated.

Risk: The skill depends on an external OCR package and local command-line tools.

Mitigation: Pin and review dependencies before installation, and verify curl, openssl, and ddddocr are supplied from trusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antarctic-penguin971/skills/donguan-interactive-login)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line examples and Python usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an interactive login workflow and writes a session cookie file when authentication succeeds.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
