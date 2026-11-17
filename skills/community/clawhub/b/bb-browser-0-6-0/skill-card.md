## Description:

Turn any website into a CLI command. 36 platforms, 103 commands — Twitter, Reddit, GitHub, YouTube, Zhihu, Bilibili, Weibo, and more. Uses OpenClaw's browser directly, no extra extension needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu-yunyu](https://clawhub.ai/user/gu-yunyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and run bb-browser site adapters for structured website data extraction through OpenClaw's browser. It is suited for collecting public or account-visible data from supported social, developer, news, finance, video, knowledge, shopping, and tool platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community adapters may be pulled from an update source that the user has not reviewed.

Mitigation: Install only when the bb-browser adapter update source is trusted, and review adapter details before running site commands.

Risk: Adapters can operate through browser sessions where the user may already be logged in, exposing account-visible, financial, work, or private data to extraction.

Mitigation: Use a separate browser profile or logged-out session for sensitive sites, and avoid running adapters against private accounts or sensitive data unless the data access is understood.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gu-yunyu/skills/bb-browser-0-6-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the bb-browser binary and generally use --openclaw; adapter outputs may be JSON and can be filtered with --jq.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json version: 0.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
