## Description: <br>
Clawbsky is an AI-powered Bluesky CLI for multi-user account management, content generation, post scheduling, analytics, RSS automation, and growth workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jyothish12345](https://clawhub.ai/user/jyothish12345) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, social-media operators, and developers use Clawbsky to manage Bluesky accounts, draft AI-assisted content, schedule posts, analyze engagement, and run RSS or growth workflows from a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live account-changing actions on a Bluesky account. <br>
Mitigation: Use a dedicated Bluesky app password and start with a test or low-risk account; review scheduled and bulk actions before running them. <br>
Risk: Reusable account sessions and local data stores may remain on disk. <br>
Mitigation: Protect local session and data files, periodically delete them when no longer needed, and rotate app passwords if a workstation may be exposed. <br>
Risk: AI features may process drafts, analytics, or account context through a configured LLM provider. <br>
Mitigation: Avoid submitting sensitive drafts or private analytics to LLM features, or use a trusted local provider for sensitive workflows. <br>


## Reference(s): <br>
- [Clawbsky on ClawHub](https://clawhub.ai/jyothish12345/skills/clawbsky) <br>
- [Bluesky App Passwords](https://bsky.app/settings/app-passwords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI commands, configuration notes, and text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bluesky credentials through BLUESKY_HANDLE and BLUESKY_APP_PASSWORD; media workflows may require ffmpeg and ffprobe.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
