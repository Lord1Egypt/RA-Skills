## Description:

Uploads local video files to Douyin Creator Center through a logged-in Chrome session, with controls for description text, visibility, publishing, and manual SMS verification handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juzanxie-dev](https://clawhub.ai/user/juzanxie-dev)

### License/Terms of Use:

MIT

## Use Case:

External creators and operators use this skill to automate upload and publication of local videos to Douyin Creator Center from an already authenticated browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Douyin Creator browser session and can upload or publish content.

Mitigation: Use an account and session with only the access needed for the upload task, review the selected video path, and use the publish toggle when human review is needed before posting.

Risk: Loose browser and page checks could expose the selected video or trigger account actions outside the intended boundary.

Mitigation: Use only a local loopback CDP endpoint, keep unrelated or suspicious tabs closed, and confirm the active Douyin Creator page before running the command.

Risk: Publishing may request SMS verification.

Mitigation: Treat SMS verification as a manual checkpoint and do not provide verification codes to automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juzanxie-dev/skills/douyin-creator-upload)
- [Douyin Creator Center upload page](https://creator.douyin.com/creator-micro/content/upload)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require an absolute local video path, Chrome CDP endpoint, authenticated Douyin Creator session, visibility option, title, and publish toggle.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
