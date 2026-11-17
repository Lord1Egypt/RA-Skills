## Description:

Extracts Bilibili video metadata, danmaku, comments, and engagement metrics, then turns them into content-operations analysis, competitor comparisons, and practical title or topic suggestions.

This skill is for research and development only.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, media planners, and creators use this skill to inspect public Bilibili videos, understand audience response, compare similar videos, and draft actionable content ideas. It is suitable for analysis and planning workflows, not real-time monitoring or sensitive decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted URLs may cause requests to unintended hosts.

Mitigation: Use only trusted Bilibili video links or direct BV/AV identifiers, and validate inputs before execution.

Risk: High-volume extraction or proxy/IP-rotation behavior may violate platform limits or trigger blocking.

Mitigation: Avoid proxy/IP rotation, keep request volume low, and follow Bilibili terms, robots guidance, and the artifact's rate-limit guidance.

Risk: Extracted comments, danmaku, uploader data, and cached files may include public-profile or user-generated data with privacy obligations.

Mitigation: Run in an isolated environment, limit retention of cached files, and handle extracted data according to applicable privacy and content policies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/if530770/skills/bilibili-video-extractor)
- [B站视频深度解析专家](references/core-workflow.md)
- [B站API调用参考（优化版）](references/bilibili-api-guide.md)
- [内容运营分析框架](references/analysis-framework.md)
- [【爆款内容拆解报告 v3.0】](references/output-template.md)
- [【竞品对比分析报告】多视频横向分析](references/competitor-analysis-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON extraction data and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public Bilibili metadata, danmaku, comments, engagement metrics, and locally cached extraction results.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
