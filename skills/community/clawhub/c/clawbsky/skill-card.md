## Description: <br>
AI-powered Bluesky CLI with multi-user auth, smart content generation, post scheduling, analytics, RSS automation, and growth tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jyothish12345](https://clawhub.ai/user/jyothish12345) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, community managers, and developers use Clawbsky to manage Bluesky accounts, generate social posts and replies, schedule content, inspect timelines, review analytics, automate RSS-driven posts, and perform account maintenance tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store Bluesky login sessions and use credentials to act on public accounts. <br>
Mitigation: Use a dedicated Bluesky app password, start with a test account when possible, and clear saved sessions after use. <br>
Risk: Automation features can post, schedule, follow, unfollow, block, mute, or otherwise change account state in bulk. <br>
Mitigation: Review commands before running them, use dry-run modes where available, and avoid aggressive growth or cleanup automation. <br>
Risk: Standalone growth and repost discovery scripts may include account or path assumptions that are not appropriate for every user. <br>
Mitigation: Inspect and edit standalone scripts such as follow-growth and discover-repost before executing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jyothish12345/skills/clawbsky) <br>
- [Publisher Profile](https://clawhub.ai/user/jyothish12345) <br>
- [Bluesky App Passwords](https://bsky.app/settings/app-passwords) <br>
- [Project Homepage](https://github.com/jyothish12345/Clawbsky) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, CLI text, JSON-capable command output, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute account-changing Bluesky actions when the user runs posting, scheduling, moderation, cleanup, RSS, or growth commands.] <br>

## Skill Version(s): <br>
2.0.13 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
