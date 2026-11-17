## Description:

Douyin (TikTok China) video uploader and automation tool for logging in, managing sessions, and uploading or publishing videos to Douyin Creator Platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancelin111](https://clawhub.ai/user/lancelin111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and automation users use this skill to log in to Douyin Creator Platform, store local session cookies, upload videos with title, description, and tags, and manage saved login data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The uploader can publish to a live Douyin account by default.

Mitigation: Use --no-publish when a draft is intended, and review title, description, tags, and account selection before allowing publication.

Risk: The skill stores Douyin login cookies and browser session data locally.

Mitigation: Keep the cookie file private, avoid sharing the skill directory after login, and use the clear command when the session is no longer needed.

Risk: Chromium is launched with reduced sandboxing and additional clipboard permissions.

Mitigation: Run the skill as a non-admin user in a dedicated workspace or isolated environment, especially when using a real Douyin account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lancelin111/skills/douyin-skill)
- [Publisher profile](https://clawhub.ai/user/lancelin111)
- [Project homepage from metadata](https://github.com/lancelin111/douyin-mcp-server)
- [Douyin Creator Platform](https://creator.douyin.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, Puppeteer, and a Chromium-compatible browser; uploads can publish by default unless --no-publish is used.]

## Skill Version(s):

0.7.0 (source: server release metadata; artifact frontmatter and package.json report 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
