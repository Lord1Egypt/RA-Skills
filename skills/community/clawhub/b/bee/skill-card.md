## Description:

抖音视频一键工作流：下载无水印视频 → 上传阿里云OSS → 写入飞书多维表格。支持各种抖音链接格式，智能提取标题和话题标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to process Douyin video links by downloading watermark-free videos, uploading them to Aliyun OSS, and writing metadata into Feishu Bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes unpinned dependent skills while handling Aliyun OSS and Feishu credentials.

Mitigation: Install only after reviewing dependent skills, prefer pinned or reviewed dependency versions, and expose only least-privilege credentials to the workflow.

Risk: Broad cloud or Feishu permissions could increase impact if the workflow or a dependency behaves unexpectedly.

Mitigation: Use scoped OSS buckets, private bucket access with signed links where appropriate, and Feishu permissions limited to the required Bitable and wiki operations.

Risk: URL and path validation are identified as areas needing tightening before use on sensitive machines.

Mitigation: Run in a constrained environment and avoid sensitive hosts until URL and path validation have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/bee)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Terminal status text with shell command usage and generated video, OSS URL, and Feishu record outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, python3, curl, dependent skills, Aliyun OSS credentials, and Feishu app credentials; supports dry-run and optional OSS or Feishu skip flags.]

## Skill Version(s):

1.2.0 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
