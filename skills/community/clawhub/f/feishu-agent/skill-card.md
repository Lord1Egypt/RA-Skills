## Description: <br>
Feishu (Lark) CLI agent that provides calendar, todo, and contact management capabilities for AI assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyd4y](https://clawhub.ai/user/boyd4y) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI assistant operators use this skill to configure and run Feishu/Lark calendar, todo, and contact commands, including scheduling meetings, checking calendars, managing Bitable todos, and searching organization contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Feishu app credentials, user access tokens, and refresh tokens in user configuration. <br>
Mitigation: Keep ~/.feishu-agent/config.json private with user-only filesystem permissions, avoid shared machines or synced backups for that file, and rotate tokens if exposed. <br>
Risk: The skill can create or delete calendar events and modify todos in a connected Feishu workspace. <br>
Mitigation: Use least-privilege Feishu app permissions and require explicit review before an assistant deletes calendar events or changes todos. <br>
Risk: The release depends on the external @teamclaw/feishu-agent package and bun runtime. <br>
Mitigation: Install only when the publisher and package source are trusted and the runtime dependency is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boyd4y/feishu-agent) <br>
- [Publisher profile](https://clawhub.ai/user/boyd4y) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun and Feishu app authorization; stores credentials and tokens in user configuration.] <br>

## Skill Version(s): <br>
1.0.14 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
