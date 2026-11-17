## Description:

Puppeteer-based Douyin (TikTok China) video uploader that helps agents log in, upload videos, manage saved login state, and publish or draft content on the Douyin Creator Platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent operators use this skill to automate Douyin Creator Platform login checks, video uploads, metadata entry, and publishing or draft creation from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically publish content to a public Douyin account by default.

Mitigation: Use --no-publish for review workflows and enable immediate publication only when the operator intentionally wants the video posted.

Risk: The skill retains local Douyin login state in cookies and browser session data.

Mitigation: Keep the skill directory private, do not commit douyin-cookies.json or chrome-user-data, and use the clear command to remove saved login data when it is no longer needed.

Risk: The browser automation launches Chromium with sandboxing disabled.

Mitigation: Run the skill as an unprivileged user in an isolated workspace and review or pin dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chongjie-ran/skills/douyin-automation)
- [Project homepage from ClawHub metadata](https://github.com/lancelin111/douyin-mcp-server)
- [Douyin Creator Platform](https://creator.douyin.com)
- [Douyin main site](https://www.douyin.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI argument guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for browser-based Douyin login, upload, draft, publish, and login-state management workflows.]

## Skill Version(s):

1.0.0 (source: release evidence, target metadata, and SKILL.md frontmatter; package.json lists 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
