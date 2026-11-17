## Description:

将财报附注中的或有事项与承诺事项整理为逐条附原文、定位锚点和来源的登记表，并按披露区分预计负债与或有负债。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向阅读中国企业财报的分析人员和审阅者，用于登记附注中的或有事项、承诺事项及相关披露，并逐条保留原文与来源定位。输出只记录披露内容；诉讼结果、会计判断和其他判断留给人工核对。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports external service activity and persistent local usage tracking, raising privacy and scope concerns.

Mitigation: Review the suspicious verdict and data handling before installation; provide nonpublic financial documents only when external processing is approved.

Risk: The security review is incomplete because one local reference could not be resolved.

Mitigation: Inspect the unresolved reference and complete the review before relying on the skill.

## Reference(s):

- [Data channel documentation](https://cuecue.cn/hub/mcp)
- [Document parsing channel documentation](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Chinese Markdown register organized into seven sections, with quoted disclosure text, location anchors, source IDs, and explicit gaps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each finding is tied to a source; missing evidence is called out for human follow-up.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
