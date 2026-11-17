## Description:

将一份简历与一份职位描述逐条对照，生成带原文引用、双向缺口和来源定位的核对报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

求职者、招聘协作者或转岗者可用它整理单份简历与单个职位描述之间可回查的文本对应关系，供人工讨论。它不用于候选人排序、评分或录用建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A report can pass format checks while containing incomplete or inaccurate matching claims, making the result seem more reliable than it is.

Mitigation: Check every quotation and source location against both originals, review all [待人工] lines, and treat PASS as a format check rather than proof of correctness.

Risk: Optional remote parsing may expose resume or job-description content to a provider whose retention practices are not verified here.

Mitigation: Prefer local processing for private resumes. Before remote parsing, confirm what documents or URLs the provider receives and how it retains them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-resume-jd-fit)
- [Cue Omni Reader parsing setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Source references, Guidance]

**Output Format:** [Four-section Markdown report with verbatim quotations, source anchors, and parse dates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One resume and one job description per report; quotations and findings require human review.]

## Skill Version(s):

0.1.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
