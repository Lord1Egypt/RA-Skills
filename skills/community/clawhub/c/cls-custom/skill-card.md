## Description:

自动获取财联社电报自定义关键词新闻并格式化为一句话新闻。

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankle1117](https://clawhub.ai/user/frankle1117)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to search 财联社电报 for user-specified keywords and turn matching items into concise, categorized one-sentence Chinese news briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically provision `agent-browser` before running.

Mitigation: Install `agent-browser` manually from a trusted, pinned source before enabling the skill.

Risk: Broad activation phrases such as generic search requests may trigger browser automation unintentionally.

Mitigation: Narrow activation phrases or require confirmation before generic searches and scheduled runs.

Risk: Browser automation against 财联社 depends on site availability and page structure.

Mitigation: Review generated summaries and update the workflow when the site layout or search behavior changes.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/frankle1117/skills/cls-custom)
- [财联社电报](https://www.cls.cn/telegraph)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Chinese news summaries, inline shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduled-run configuration and grouped one-sentence news items.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
