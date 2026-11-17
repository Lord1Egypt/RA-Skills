## Description:

将一份境内债券发行文件整理为带原文引句和来源锚点的八项条款卡，并将估值和评级判断留待人工处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要核对境内债券发行条款的用户，依据其提供的募集说明书、发行方案或公告整理发行人、规模期限、利率、增信、赎回回售、披露和违约条款，并保留原句与定位。

### Deployment Geography for Use:

China (Mainland)

## Known Risks and Mitigations:

Risk: Optional external data and attachment services use a credential and may process bond documents.

Mitigation: Use the supplied-document path when external lookup or parsing is unnecessary; protect CUE_API_KEY and only submit documents approved for the chosen service.

Risk: Bond terms or citations may be incomplete or inaccurate, especially when source documents or service analysis are incomplete.

Mitigation: Check each quoted term and its source anchor against the original prospectus or issue document; leave missing items explicit and keep valuation and rating judgments for human review.

Risk: Installation sources are not pinned.

Mitigation: Review the installation source and pin it to a reviewed release or revision before installation.

## Reference(s):

- [债券层级与来源定位参考](artifact/references/bond-layers.md)
- [ClawHub 技能发布页](https://clawhub.ai/huhoo/skills/cue-bond-terms-cn)
- [Cue 数据服务配置](https://cuecue.cn/hub/mcp)
- [Cue 附件解析配置](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown bond terms card with verbatim quotes, source anchors, missing-item notes, and human-review flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight named terms; unavailable details remain marked as not found, and valuation or rating judgments are left for human review.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata; frontmatter agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
