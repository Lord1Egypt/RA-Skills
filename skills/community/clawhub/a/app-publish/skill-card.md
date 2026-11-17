## Description:

Automates video upload and posting to Kuaishou, Bilibili, and Douyin through Chrome browser scripts, including title, cover, keyword entry, and login checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohei2022](https://clawhub.ai/user/xiaohei2022)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators use this skill to fill video metadata, upload video and cover files, and publish or preview posts across Kuaishou, Bilibili, and Douyin from a TXT configuration file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish video posts to logged-in creator accounts by default.

Mitigation: Run commands with --no-publish first, review the browser state manually, and only publish after each platform workflow is verified.

Risk: The Kuaishou workflow can discard an existing draft or cached draft prompt while preparing a post.

Mitigation: Use an isolated Chrome profile or manually review the Kuaishou page before running full publishing commands.

Risk: Credential-bearing proxy URLs may be exposed if proxy environment variables are logged.

Mitigation: Avoid credential-bearing proxy URLs unless logs are protected or the skill is updated to redact proxy values.

Risk: The skill reuses logged-in Chrome sessions, which can affect active creator account state.

Mitigation: Use a dedicated Chrome user data directory for testing and clear or isolate the profile when account session reuse is not desired.

## Reference(s):

- [ClawHub App Publish Listing](https://clawhub.ai/xiaohei2022/skills/app-publish)
- [Kuaishou Creator Service Platform](https://cp.kuaishou.com/)
- [Bilibili Video Upload](https://member.bilibili.com/platform/upload/video/frame)
- [Douyin Creator Upload](https://creator.douyin.com/creator-micro/content/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with CLI commands and JSON status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads TXT configuration files and supports --no-publish preview runs before posting.]

## Skill Version(s):

1.0.5 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
