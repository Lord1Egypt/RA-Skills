## Description:

Monitor RSS feeds, blogs, and news sources with AI-powered summarization and generate daily digests in Markdown or console output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[su707181393-del](https://clawhub.ai/user/su707181393-del)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to monitor trusted RSS feeds, blogs, and news sources, summarize newly discovered articles, and produce recurring digests for research, competitive intelligence, trend tracking, or content curation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool fetches configured feed and article URLs without clear network safeguards.

Mitigation: Use only trusted public feed URLs, avoid internal or private-network sources, and run it in a network-restricted environment until URL allowlisting and private-network blocking are added.

Risk: Generated Markdown may contain untrusted article titles, links, authors, or summaries.

Mitigation: Review generated digests before sharing and avoid rendering them in permissive Markdown viewers unless output escaping or sanitization is added.

Risk: Documentation mentions Feishu, email, and cron delivery behavior that is not fully implemented in the CLI artifact.

Mitigation: Confirm delivery features in the installed package before relying on them, or limit use to the implemented add, remove, list, run, and config commands.

## Reference(s):

- [Content Watcher ClawHub skill page](https://clawhub.ai/su707181393-del/skills/content-watcher)
- [Publisher profile](https://clawhub.ai/user/su707181393-del)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest, console text, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write digest Markdown to a user-specified output file and stores local configuration under ~/.config/content-watcher/config.json.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
