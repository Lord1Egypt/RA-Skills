## Description:

Fetch social media content and save it to Obsidian vaults across Twitter/X, Reddit, GitHub, HackerNews, Bilibili, Weibo, Xiaohongshu, and other bb-browser supported platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glassmarbles](https://clawhub.ai/user/glassmarbles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run social-feed syncs that collect selected accounts and save filtered, tagged posts as Obsidian Markdown notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party global bb-browser dependency while using the logged-in OpenClaw browser session.

Mitigation: Pin and verify the dependency before use, run with a minimal environment, and avoid using broader account access than the sync requires.

Risk: The sync writes fetched social content into the configured Obsidian vault and persists local sync state.

Mitigation: Use a dedicated vault or folder, confirm vault_base before running, and run with --dry-run before the first write.

Risk: Scheduled sync can repeatedly collect and save content from configured accounts.

Mitigation: Review any cron entry before enabling scheduled sync, confirm the account list and schedule, and remove jobs that are no longer needed.

Risk: Incorrect platform usernames or filter settings can collect or retain unintended content.

Mitigation: Validate account identifiers, blocked keywords, and tagging rules before enabling regular sync.

## Reference(s):

- [Supported Platforms](references/platforms.md)
- [bb-sites](https://github.com/epiral/bb-sites)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with YAML configuration examples and shell commands; runtime sync writes Obsidian Markdown files with YAML frontmatter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated notes are organized under vault_base/@username/, and incremental sync state is stored in .claw-social-feed-state.json.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
