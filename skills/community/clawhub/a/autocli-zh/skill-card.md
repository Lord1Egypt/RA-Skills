## Description:

AutoCLI zh guides agents in Simplified Chinese to use the autocli CLI for supported websites, desktop applications, and external CLIs, including read workflows and user-confirmed write actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poiskgit](https://clawhub.ai/user/poiskgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent route supported browsing, search, timeline, bookmark, notification, article, and CLI-backed tasks through AutoCLI. It is especially useful when the user wants concise Chinese-language results while preserving confirmation gates for write actions, browser-session debugging, and persistent adapter changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some AutoCLI targets may read account-backed pages through an existing browser session.

Mitigation: Use those workflows only when the user is comfortable with AutoCLI reading the requested logged-in pages, and obtain consent before browser-session debugging or bridge-state inspection.

Risk: Write actions such as posting, replying, liking, following, deleting, or subscribing may be externally visible or irreversible.

Mitigation: Require explicit user confirmation of the target object and submitted content before executing any write action.

Risk: Custom adapters and plugin configuration can persist changes under ~/.autocli.

Mitigation: Explain the persistent file paths and get user approval before creating or modifying adapters, plugins, or external CLI configuration.

## Reference(s):

- [AutoCLI upstream project](https://github.com/nashsu/AutoCLI)
- [Bilibili target reference](references/bilibili.md)
- [Google target reference](references/google.md)
- [Hacker News target reference](references/hackernews.md)
- [Mtime target reference](references/mtime.md)
- [Twitter / X target reference](references/twitter.md)
- [Wikipedia target reference](references/wikipedia.md)
- [Fallbacks guide](guides/fallbacks.md)
- [Custom adapters guide](guides/custom-adapters.md)
- [Custom adapters reference](guides/custom-adapters-reference.md)
- [Reference bootstrap guide](guides/reference-bootstrap.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Simplified Chinese Markdown with inline shell commands and optional JSON-oriented command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes concise summaries over raw command dumps; supported read operations may use structured JSON output when useful.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
