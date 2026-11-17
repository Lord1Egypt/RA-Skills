## Description:

Send images to Feishu users through the Feishu Open Platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombfuock](https://clawhub.ai/user/bombfuock)

### License/Terms of Use:


## Use Case:

Developers and automation users can send a local image file to a Feishu user from shell or Python workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships reusable Feishu app credentials in plaintext.

Mitigation: Do not install this version unless the publisher's Feishu app identity is trusted; the publisher should revoke and rotate the exposed secret and require user-supplied secure configuration.

Risk: Local image paths provided to the scripts are uploaded to Feishu and sent under the bundled app identity.

Mitigation: Confirm the target user and image file before use, and add clear confirmation and input validation before sending files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bombfuock/skills/feishu-img-send)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu image upload endpoint](https://open.feishu.cn/open-apis/im/v1/images)
- [Feishu image message endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Shell output or Python return data from Feishu API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads local image files to Feishu and returns the API response.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
