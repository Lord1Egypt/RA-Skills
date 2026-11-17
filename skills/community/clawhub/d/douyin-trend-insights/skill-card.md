## Description:

当用户需要做抖音趋势洞察、抖音趋势分析、热点观察、内容方向判断、趋势线索归纳或营销灵感整理时使用。面向内容运营、品牌调研和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营人员、品牌调研者和创作者可用它查看抖音热榜或按关键词搜索内容，并整理趋势信号、内容样本与后续分析角度。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly uses an unpinned, mutable CLI package; a compromised future release could expose credentials or accessible local resources.

Mitigation: Review the package before installation and run it with only the files and credentials needed for the task.

Risk: Search terms and filters are sent to SocialDataX, and the security scan was partial because some local references could not be resolved.

Mitigation: Avoid sensitive search terms and review unresolved references before using the skill in a credential-bearing environment.

## Reference(s):

- [SocialDataX API key access](https://socialdatax.com/ai?from=clawhub)
- [SocialDataX billing](https://socialdatax.com/dashboard/billing)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Markdown summaries; CLI results are returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include rankings, heat signals, titles, creators, links or content IDs, and follow-up angles.]

## Skill Version(s):

0.1.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
