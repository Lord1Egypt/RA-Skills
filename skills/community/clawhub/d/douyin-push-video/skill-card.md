## Description:

Helps agents guide and perform Douyin video publishing using local video files, OAuth credentials, and Douyin Open Platform upload and create APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15027302155](https://clawhub.ai/user/15027302155)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare local videos, obtain or configure Douyin OAuth credentials, and publish videos to an authorized Douyin account through manual guidance or the provided Node.js scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Douyin account tokens in plaintext with weak safeguards.

Mitigation: Review before installing with real credentials, use throwaway or narrowly scoped tokens where possible, restrict .env file permissions, and rotate or revoke tokens after use.

Risk: Credential helpers can expose tokens in terminal logs or CI output.

Mitigation: Avoid running token exchange helpers in logged terminals or CI and do not commit .env files.

## Reference(s):

- [Douyin Open Platform](https://partner.open-douyin.com/)
- [Douyin Authorization Code Documentation](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/douyin-get-permission-code)
- [Douyin Access Token Documentation](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/get-access-token)
- [ClawHub Skill Page](https://clawhub.ai/15027302155/skills/douyin-push-video)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local .env file when the user asks to store Douyin credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
