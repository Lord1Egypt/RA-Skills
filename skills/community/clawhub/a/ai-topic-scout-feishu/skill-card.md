## Description:

AI Topic Scout Feishu helps an agent collect public YouTube and Twitter/X content, analyze cross-platform AI topic trends, score topic heat, and write reports into Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdimtech](https://clawhub.ai/user/xdimtech)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, analysts, and agent operators use this skill to monitor configured AI-focused YouTube channels and Twitter/X accounts, identify recurring topics, and maintain a Feishu Bitable with raw content and topic-analysis records. The agent can also initialize tables, manage data sources, run scheduled collection, and return ranked topic summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured sources, fetched posts, generated analysis, and Feishu records may pass through YouTube, Nitter mirrors, the configured LLM provider, web search, and Feishu.

Mitigation: Use a dedicated environment, review Feishu OAuth permissions, avoid private or sensitive accounts, and restrict access to the target Feishu tables.

Risk: The helper scripts execute external tools and contact public content platforms, which can be affected by tool version changes, platform limits, or unstable mirrors.

Mitigation: Pin or review yt-dlp versions, avoid sudo where possible, configure official API tokens when appropriate, and reduce fetch frequency when limits are encountered.

Risk: Scheduled runs can repeatedly update the wrong table or source list if automation is enabled before setup is verified.

Mitigation: Enable cron only after confirming the Feishu Bitable target, source records, and fetch settings are correct.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xdimtech/skills/ai-topic-scout-feishu)
- [Publisher profile](https://clawhub.ai/user/xdimtech)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Configuration example](config.example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style conversational summaries, JSON from helper scripts, YAML configuration, and Feishu Bitable records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates Feishu Bitable apps, tables, fields, and records; helper scripts fetch bounded public content for configured sources.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
