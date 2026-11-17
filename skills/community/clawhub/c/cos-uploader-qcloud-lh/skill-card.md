## Description:

Receives photos through WeChat via OpenClaw and uploads them to Tencent Cloud COS, organized by year and month.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingronzhao](https://clawhub.ai/user/jingronzhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to receive photo messages from WeChat and archive the corresponding image files into a configured Tencent Cloud COS bucket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted OpenClaw attachment metadata or debug use can cause arbitrary readable local files to be uploaded.

Mitigation: Accept only trusted OpenClaw attachment metadata or restrict resolved paths to the inbound media directory, reject symlinks, verify actual image content, and run the skill as a dedicated low-privilege user.

Risk: COS credentials can allow broader storage access than the uploader needs.

Mitigation: Use a Tencent Cloud sub-account limited to writing only the intended bucket and prefix.

Risk: People sending images may not expect their photos to be stored in Tencent Cloud COS.

Mitigation: Make the storage behavior clear to users before deployment and operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jingronzhao/skills/cos-uploader-qcloud-lh)
- [Tencent Cloud COS bucket console](https://console.cloud.tencent.com/cos/bucket)
- [Tencent Cloud CAM API key console](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text upload status or error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include COS object path, file size, and configured storage class when upload succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
