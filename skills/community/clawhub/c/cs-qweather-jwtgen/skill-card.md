## Description:

和风天气 JWT Token 生成工具。当需要生成、刷新和风天气 API 的 JWT 认证 Token 时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[savior1987](https://clawhub.ai/user/savior1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate or refresh JWT authentication tokens for QWeather API workflows with an EdDSA private key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a QWeather private key and account identifiers from local files and environment variables.

Mitigation: Keep ~/.myjwtkey/ed25519-private.pem and ~/.openclaw/.env private, user-owned, and free of unrelated secrets.

Risk: The skill overwrites ~/.myjwtkey/last-token.dat when generating a token.

Mitigation: Run it only in the intended user environment and confirm dependent QWeather workflows should consume the refreshed token.

Risk: The skill writes masked operational logs under /tmp/cslog.

Mitigation: Review local log access controls and avoid placing unmasked secrets in related environment files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated JWT text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated token to ~/.myjwtkey/last-token.dat and masked logs to /tmp/cslog.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
