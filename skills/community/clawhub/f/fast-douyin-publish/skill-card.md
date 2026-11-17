## Description:

Fast Douyin Publish helps agents upload videos to Douyin with QR-code login, title and tag entry, and local publishing history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadlining](https://clawhub.ai/user/deadlining)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and automation operators use this skill to publish local video files to Douyin with supplied titles, tags, and optional descriptions. The skill is intended for workflows where the operator can review the video and metadata before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Douyin login sessions are stored locally in plaintext.

Mitigation: Run the skill from a private, isolated workspace; protect or delete config/cookies/douyin.json after use; and do not commit cookie files.

Risk: Publishing in headless mode can post video content and metadata without visual confirmation.

Mitigation: Use visible browser mode until the exact video, title, tags, and description have been reviewed.

Risk: The bundled account configuration includes enabled non-Douyin platform entries despite the skill being scoped to Douyin.

Mitigation: Remove unused account entries from config/accounts.json unless they are intentionally needed.

Risk: Publish logs and error screenshots can expose account, content, or operational details.

Mitigation: Keep config/publish_log.json and error_debug.png out of source control and delete them when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deadlining/skills/fast-douyin-publish)
- [ClawHub publisher profile](https://clawhub.ai/user/deadlining)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON publish logs and Playwright browser session state during use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
