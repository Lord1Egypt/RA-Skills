## Description: <br>
Daily automated health check + mood tracking + proactive alerts for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lalawgwg99](https://clawhub.ai/user/lalawgwg99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate daily status, mood, and task reports for an OpenClaw workspace, with optional scheduled delivery to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save OpenClaw workspace status, task summaries, and mood-derived report data locally. <br>
Mitigation: Install only if local report storage is acceptable for the workspace, and review generated report files before sharing them. <br>
Risk: After Telegram is configured and cron entries are added, reports may be sent on an unattended recurring schedule. <br>
Mitigation: Keep the placeholder chat ID or disable Telegram for local-only use, and add cron entries only when recurring delivery is intended. <br>


## Reference(s): <br>
- [Daily-Observatory Lite on ClawHub](https://clawhub.ai/lalawgwg99/daily-observatory-lite) <br>
- [Project homepage from skill metadata](https://github.com/lalawgwg99/daily-observatory-lite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style daily reports, terminal text, configuration guidance, and optional Telegram messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved locally under the skill memory directory and delivered through Telegram only after the user configures a real chat ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
