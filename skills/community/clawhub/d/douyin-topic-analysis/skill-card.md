## Description:

当用户需要做抖音选题、抖音内容选题、短视频选题策划、爆款角度拆解、内容方向规划或选题素材整理时使用。面向内容运营、品牌调研和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

面向内容运营人员、品牌研究者和创作者，用关键词或选题方向查找抖音内容样本，并整理相关角度、热度信号和后续追问方向。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions run an unpinned CLI package with automatic acceptance; that package can change between runs and may access the configured API key.

Mitigation: Review the package and credential instructions before running it, and use a trusted environment for any configured key.

Risk: Search terms and filters may be sent to SocialDataX, and the security scan had incomplete coverage because some local references could not be resolved.

Mitigation: Avoid sensitive search terms and review the skill and its unresolved references before installation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Markdown analysis of Douyin search results; CLI results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include content titles, authors or accounts, links or IDs, and follow-up angles; search supports optional filters and paging.]

## Skill Version(s):

0.1.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
