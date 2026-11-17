## Description:

支持自定义分支/代码库创建MR、查询MR合并状态、按代码库+环境关键字触发发布流水线，并自动推送通知。支持自然语言输入，由大模型自动识别意图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[farb](https://clawhub.ai/user/farb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to create and inspect Alibaba Cloud Yunxiao merge requests, trigger repository and environment-specific pipelines, and send operational notifications from natural language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create merge requests or trigger deployment pipelines from LLM-parsed natural language without confirmation.

Mitigation: Require explicit confirmation before MR creation or deployment, and allowlist repositories, branches, and pipeline IDs.

Risk: Yunxiao and webhook credentials can grant operational access if over-scoped or exposed.

Mitigation: Use a least-privilege Yunxiao token, scope it away from production pipelines where possible, and configure only trusted webhook endpoints.

Risk: The manifest points to a Python file name that is not shipped with this artifact.

Mitigation: Fix the manifest main entry to point to the shipped Python file before installation or execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also trigger Yunxiao API actions and webhook notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
