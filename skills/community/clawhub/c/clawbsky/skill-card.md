## Description:

AI-powered Bluesky CLI with multi-user auth, smart content generation, post scheduling, analytics, RSS automation, and growth tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jyothish12345](https://clawhub.ai/user/jyothish12345)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and automation-focused Bluesky users use Clawbsky to manage accounts, generate and schedule posts, read timelines, analyze engagement, process RSS feeds, and run growth or moderation workflows from a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live Bluesky account actions including posting, following, unfollowing, blocking, muting, reposting, scheduling, RSS fetching, webhook delivery, and LLM-assisted content processing.

Mitigation: Use a dedicated test account or app password, review actions before running bulk workflows, and prefer dry-run or manual confirmation paths when available.

Risk: The skill handles durable Bluesky credentials and local session state.

Mitigation: Use a Bluesky app password rather than the main account password, limit account privileges where possible, and inspect stored sessions under local .config paths.

Risk: RSS feeds, webhooks, and LLM endpoints can introduce untrusted external content or destinations into automation workflows.

Mitigation: Configure only trusted RSS sources, webhook URLs, and LLM endpoints; review generated content before publishing.

## Reference(s):

- [Clawbsky on ClawHub](https://clawhub.ai/jyothish12345/skills/clawbsky)
- [Clawbsky GitHub repository](https://github.com/jyothish12345/Clawbsky)
- [Bluesky app passwords](https://bsky.app/settings/app-passwords)
- [clawbskyweb dashboard companion](https://github.com/jyothish12345/clawbskyweb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands, JSON options, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUESKY_HANDLE, BLUESKY_APP_PASSWORD, ffmpeg, and ffprobe for the documented OpenClaw environment; AI features may use configured LLM providers.]

## Skill Version(s):

2.0.13 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
