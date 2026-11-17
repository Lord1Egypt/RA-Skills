## Description:

抓取主流中外 AI 资讯源生成中文 markdown 日报。用户说"生成今日 AI 日报"/"今天有什么 AI 新闻"等指令时启用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yan1sanjin](https://clawhub.ai/user/yan1sanjin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and AI practitioners use this skill to collect daily AI industry signals from international and Chinese sources, verify source quality, and produce a concise Chinese Markdown news digest. It is useful for recurring local news briefings in agent runtimes such as Claude Code, Cursor, Codex, OpenClaw, and Gemini CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install commands may execute or install mutable remote code or instructions without verification.

Mitigation: Review the skill before installing and prefer manual installation of the reviewed SKILL.md or a pinned, checksum-verified release.

Risk: The skill fetches public web sources and creates or updates files under the configured ai-news output directory.

Mitigation: Run it in an agent environment where web access and file writes are expected, and confirm the configured output path before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yan1sanjin/skills/ai-news-digest-cn)
- [ClawHub publisher profile](https://clawhub.ai/user/yan1sanjin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown digest written to a local .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a dated local digest, supports path, mode, and region parameters, and includes source credibility markers plus fetch failure notes.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
