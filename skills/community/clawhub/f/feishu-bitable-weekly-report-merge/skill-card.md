## Description:

飞书多维表格周报权限检查与合并一体化工具：读取用户提供的多维表格 URL，检查周报文档权限，并在用户确认后合并可访问文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ganguagua](https://clawhub.ai/user/ganguagua)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using Feishu Bitable weekly reports use this skill to extract report links, identify accessible and inaccessible documents, and create one merged Feishu document after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accessible weekly report contents may be copied into a newly merged Feishu document.

Mitigation: Review the source table and accessible document list before confirming the merge.

Risk: Permission failures or Feishu rate limits can lead to an incomplete merge set.

Mitigation: Use the reported accessible and inaccessible lists, and retry rate-limited document fetches before creating the final document.

## Reference(s):

- [Merge Rules Reference](artifact/references/merge_rules.md)
- [Permission Rules Reference](artifact/references/permission_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown/text response with Feishu document link when a merge is created]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports accessible and inaccessible document lists; creates the merged Feishu document only after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
