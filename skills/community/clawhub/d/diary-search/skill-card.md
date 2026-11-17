## Description:

Searches OpenClaw diary entries and conversation history with Chinese tokenization, BM25 search, time-decay ranking, session export, cleanup review, and cron run lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebrinass](https://clawhub.ai/user/sebrinass)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to search personal diary files, review past agent sessions including archived sessions, export readable session records, inspect cron run history, and preview cleanup of duplicate checkpoint backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private diary, conversation, cron, and OpenClaw configuration data.

Mitigation: Install only from a trusted publisher, review the package version before use, and grant access only in environments where those records may be searched.

Risk: The skill is installed as global npm code, so updates or package changes can alter behavior.

Mitigation: Use a pinned, reviewed package version and re-review before upgrading.

Risk: Cleanup operations can remove checkpoint backup files from session directories.

Mitigation: Run cleanup in dry-run mode first and proceed only after explicit user confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sebrinass/skills/diary-search)
- [npm package: diary-search](https://www.npmjs.com/package/diary-search)
- [GitHub link declared in skill documentation](https://github.com/sebrinass/diary-search)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown or plain text results for search hits, statistics, session exports, cron runs, and cleanup previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session exports are written as Markdown files with YAML metadata and a default three-day expiration.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
