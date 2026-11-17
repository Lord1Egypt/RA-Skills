## Description:

收集 Moltbook 热门内容，过滤去重后生成包含 AI 深度分析的结构化日报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyzengfen](https://clawhub.ai/user/happyzengfen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate Moltbook daily reports from configured source data, add structured AI analysis, and publish the report to GetNote or optional email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill concentrates Moltbook, GetNote, and optional SMTP credentials in local configuration.

Mitigation: Use narrowly scoped Moltbook and GetNote credentials, avoid storing SMTP passwords in the provided .env file, and restrict local configuration file permissions.

Risk: Generated reports can be uploaded to external services through GetNote or optional email delivery.

Mitigation: Inspect generated reports before upload and keep external publishing disabled until upload behavior, logging, and rollback expectations are explicit.

Risk: Scheduled execution can automate external uploads before runtime behavior has been reviewed.

Mitigation: Avoid enabling the cron job until logging and external-upload behavior are reviewed and reversible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happyzengfen/skills/fengxinzi-moltbook)
- [ClawHub publisher profile](https://clawhub.ai/user/happyzengfen)
- [Moltbook](https://www.moltbook.com/)
- [Moltbook API documentation](https://www.moltbook.com/api/docs)
- [GetNote developer site](https://open.getnote.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with shell command and environment configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a dated Moltbook report with filtered items, AI analysis sections, and source metadata; may save content to GetNote when credentials are configured.]

## Skill Version(s):

1.0.0 (source: evidence.json release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
