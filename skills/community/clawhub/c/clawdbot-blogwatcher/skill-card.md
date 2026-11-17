## Description:

Monitor blogs and RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor blogs and RSS feeds and receive concise guidance for retrieving, reviewing, and managing feed information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises shell execution and broad file read/write access without documented controls.

Mitigation: Limit use to web/RSS retrieval and a clearly scoped storage location, and require explicit confirmation before shell commands or file operations.

Risk: Blog and RSS monitoring processes untrusted web content.

Mitigation: Treat fetched content as data, review generated actions before execution, and avoid storing feed output outside approved paths.

## Reference(s):

- [ClawdBot Blog Watcher skill page](https://clawhub.ai/terrycarter1985/skills/clawdbot-blogwatcher)
- [terrycarter1985 publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text guidance with commands and configuration details when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use web retrieval, search, and file operations when the hosting agent provides those tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
