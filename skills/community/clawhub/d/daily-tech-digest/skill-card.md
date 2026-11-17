## Description:

每日科技热点简报生成器。自动收集AI、数码、科技领域时事热点，整理到Obsidian，推送到手机负一屏。支持定时任务和手动触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajawpwinner-del](https://clawhub.ai/user/ajawpwinner-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect daily AI, digital product, and technology news, summarize articles, organize the results into Obsidian notes, and push a short digest to a phone feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic Git sync can push the full Obsidian vault, including unintended private notes, to a remote repository.

Mitigation: Use a dedicated vault or repository, review the sync target, and disable or narrow the automatic Git push before scheduling the skill.

Risk: The organizer rewrites archive notes and deletes the original daily digest after creating an index, which can cause data loss if parsing or categorization is wrong.

Mitigation: Keep backups and test organizer runs on a copy of the vault before enabling recurring execution.

Risk: The skill depends on other local skills for news collection and phone-feed push behavior.

Mitigation: Confirm the dependent skills are installed and trusted before running the scripts or enabling OpenClaw cron jobs.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/ajawpwinner-del/skills/daily-tech-digest)
- [Publisher profile](https://clawhub.ai/user/ajawpwinner-del)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, phone-feed summaries, shell command examples, and JSON execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates dated Obsidian digest and archive files; can run manually or through scheduled OpenClaw cron commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
