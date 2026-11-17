## Description:

Automatically scrapes, categorizes, summarizes, archives, and optionally delivers X bookmark insights to a configured messaging channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adambrainai](https://clawhub.ai/user/adambrainai)

### License/Terms of Use:


## Use Case:

External users and personal productivity agents use this skill to turn saved X bookmarks into categorized summaries, searchable local archives, and optional daily delivery through Discord, Slack, Telegram, email, or file-only workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process private X bookmark data, stored sessions, and local archives.

Mitigation: Review before installing, prefer file-only mode for sensitive bookmarks, and avoid browser-cookie access unless the account risk is understood.

Risk: The documented setup uses an unpinned global bird-cli install for X bookmark access.

Mitigation: Use a vetted, pinned, project-local bird-cli installation before enabling bookmark collection.

Risk: Webhook delivery can expose bookmark summaries or secrets if URLs are stored in files or committed.

Mitigation: Keep webhook URLs in environment variables and do not commit delivery credentials to files.

Risk: Scheduled analysis can continue running after setup.

Mitigation: Review and remove cron or heartbeat entries when recurring bookmark processing is no longer wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adambrainai/skills/adhd-bookmark-analyzer)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [bookmark-rules.md](artifact/bookmark-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files, Shell commands, Configuration guidance]

**Output Format:** [Markdown or text summaries, JSON archive files, and inline shell/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local bookmark archives and may send summaries through configured external delivery channels.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
