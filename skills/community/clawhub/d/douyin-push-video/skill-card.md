## Description: <br>
Assists users with publishing local or user-provided videos to a Douyin account, including OAuth credential setup, upload guidance, API-based posting, and pre-publication checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15027302155](https://clawhub.ai/user/15027302155) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to prepare Douyin OAuth credentials, upload a video, and publish it through manual steps or Douyin Open Platform API workflows. It is intended for account-authorized posting where the user can confirm the account, video, caption, and visibility before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Douyin account tokens may be stored in plaintext in a local .env file. <br>
Mitigation: Use short-lived environment variables or a secret manager where possible, keep .env out of source control, and rotate or revoke tokens after use. <br>
Risk: The skill can publish to a real Douyin account with limited safeguards. <br>
Mitigation: Confirm the exact account, video file, caption, tags, and visibility before running any posting script or API workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/15027302155/douyin-push-video) <br>
- [Douyin Open Platform](https://partner.open-douyin.com/) <br>
- [Douyin Authorization Code Documentation](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/douyin-get-permission-code) <br>
- [Douyin Access Token Documentation](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/get-access-token) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or update of a local .env file containing Douyin OAuth credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
