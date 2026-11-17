## Description:

Summarizes videos from a user's Bilibili favorites by reading subtitles, comments, and danmaku, then producing bilingual structured study notes and PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mistake-12](https://clawhub.ai/user/mistake-12)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to select Bilibili favorites, fetch video metadata and discussion content, generate bilingual summaries, track processed videos, search past summaries, and optionally produce PDF study notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses reusable Bilibili session cookies.

Mitigation: Keep the .env file private, restrict file permissions such as chmod 600 where applicable, avoid sharing logs that include cookie prefixes, and refresh cookies when they expire or may have been exposed.

Risk: Generated PDFs can be sent through third-party chat or messaging platforms when delivery is enabled.

Mitigation: Leave delivery set to none unless outbound sharing is intentional, and review the destination and summary contents before sending.

Risk: Summaries, processing history, topic data, and vector-search data can persist locally under the skill data directory.

Mitigation: Periodically review or delete local data such as processed history and vector indexes when long-term retention is not needed.

Risk: Scheduled runs can continue using the user's Bilibili cookies in the background.

Mitigation: Enable cron or scheduled execution only when intended, and audit or remove scheduled jobs that are no longer needed.

Risk: The release pins dependencies that may need maintenance before regular use.

Mitigation: Review and update pinned dependencies as part of installation or ongoing operational maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mistake-12/skills/bilibili-reader-skill)
- [Bilibili API notes](artifact/references/bilibili-api-notes.md)
- [Installing external skills reference](artifact/references/installing-external-skills.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, JSON summary data, shell commands, local PDF files, and optional delivery instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bilingual video summaries, local processing history, optional ChromaDB indexes, and optional outbound delivery prompts.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
