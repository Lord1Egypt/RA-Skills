## Description:

Turn any website into a CLI command. 36 platforms, 103 commands - Twitter, Reddit, GitHub, YouTube, Zhihu, Bilibili, Weibo, and more. Uses OpenClaw's browser directly, no extra extension needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a1437707640-ui](https://clawhub.ai/user/a1437707640-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run bb-browser website adapters through OpenClaw's browser, extracting structured data from social, developer, finance, news, knowledge, and video sites. It also guides users toward listing, filtering, inspecting, and creating adapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community website adapters may access the same browser session and logged-in account context used by OpenClaw.

Mitigation: Review adapter source before execution and use a separate browser profile or logged-out session when working with sensitive accounts.

Risk: Release provenance is unavailable, so upstream source history cannot be confirmed from server-resolved GitHub import data.

Mitigation: Treat the packaged artifact and server evidence as the review boundary, and avoid inferring provenance from skill text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a1437707640-ui/skills/bb-browser-openclaw)
- [Publisher profile](https://clawhub.ai/user/a1437707640-ui)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and structured command-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to use bb-browser with --openclaw; some adapters may return JSON for downstream filtering.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
