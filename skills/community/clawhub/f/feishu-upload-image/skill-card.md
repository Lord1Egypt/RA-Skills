## Description:

Uploads a local image to Feishu and returns the image_key needed to send that image through Feishu IM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkzleond](https://clawhub.ai/user/jkzleond)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a local image must be uploaded to Feishu before composing a Feishu IM image message. It returns only the Feishu image_key and does not send the message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials and cached app tokens may be exposed if stored or cached in under-protected locations.

Mitigation: Install only for trusted publishers, keep credentials in protected user-owned configuration, and move or remove token caching before production use.

Risk: Selected local images are uploaded to Feishu, which may disclose image contents outside the local environment.

Mitigation: Review image sensitivity, Feishu workspace permissions, and approval requirements before upload.

Risk: Credential parsing needs review before production use.

Mitigation: Harden credential parsing and document the required secret-handling scope before deployment.

## Reference(s):

- [Feishu Open APIs](https://open.feishu.cn/open-apis)
- [ClawHub Skill Page](https://clawhub.ai/jkzleond/skills/feishu-upload-image)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text Feishu image_key string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one image_key for one selected local image; credentials are required for the Feishu upload request.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
