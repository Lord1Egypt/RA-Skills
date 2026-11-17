## Description:

抖音创作者中心评论管理助手。通过 Playwright 浏览器自动化抓取评论并批量回复，支持智能模板匹配和交互式可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, MCN operators, e-commerce account managers, and operations staff use this skill to collect Douyin Creator Center comments, prepare or execute template-based replies, and generate HTML comment-analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post bulk replies from a live Douyin creator account with weak confirmation and unsafe targeting safeguards.

Mitigation: Run dry-run first, manually verify the target comments and reply plan, keep per-run limits low, and avoid live batch reply until targeting and confirmation safeguards are fixed.

Risk: The skill reuses a persistent Douyin login profile.

Mitigation: Keep the .playwright profile private, exclude it from source control and backups, and run the skill only in a workspace intended for that account.

Risk: Generated reports and live workflows may expose or act on creator-account comment data.

Mitigation: Review generated JSON and HTML locally before sharing, avoid sensitive workspaces, and do not rely on the HTML report for untrusted content until escaping protections are fixed.

## Reference(s):

- [抖音开放平台 - 评论管理 API 参考](references/douyin-api.md)
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/douyin-comment-manager)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, HTML reports]

**Output Format:** [Markdown guidance with shell commands; generated workflow artifacts are JSON files and an HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Playwright browser automation, reply templates, dry-run previews, per-run reply limits, and persistent local Douyin session state.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
