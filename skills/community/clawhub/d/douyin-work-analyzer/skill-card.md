## Description:

分析用户指定的单个抖音视频或图文作品，根据经授权浏览器中可见的页面信息生成内容分析及 Markdown 和 JSON 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和分析人员可用此技能复核单个指定的抖音视频或图文作品，提炼其可见信息、内容结构、亮点和问题，并导出便于阅读和后续处理的报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this skill suspicious because it may delete existing reports before a replacement succeeds; inspection of the main script was incomplete.

Mitigation: Use a new or empty output directory and keep backups; obtain a complete script review and clarify the browser tool scope before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xxjrq/skills/douyin-work-analyzer)
- [Publisher profile](https://clawhub.ai/user/xxjrq)
- [Easy WebBridge documentation and source](https://github.com/xxjrq/easy-webbridge)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown and JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One specified work per run; uncertain facts remain empty and page evidence limits are reported.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
