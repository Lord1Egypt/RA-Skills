## Description: <br>
Checks OpenAI Codex CLI daily and weekly rate limit status using local session logs, with optional fresh checks through the codex CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Codex users use this skill to check cached or refreshed Codex quota status before heavy work, diagnose rate-limit symptoms, and compare quota across saved accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The all-accounts mode temporarily rewrites ~/.codex/auth.json to switch saved Codex accounts. <br>
Mitigation: Use --all --yes only when no other Codex processes are running, and keep a backup of auth.json before running it. <br>
Risk: The all-accounts report is written to /tmp/codex-quota-all.json and can contain sensitive account metadata. <br>
Mitigation: Delete the report after use or move it to a private directory with appropriate file permissions. <br>
Risk: The skill reads local Codex session logs to extract rate-limit data. <br>
Mitigation: Install and run it only in environments where reading ~/.codex/sessions is acceptable. <br>


## Reference(s): <br>
- [Codex Quota ClawHub listing](https://clawhub.ai/odrobnik/codex-quota) <br>
- [Project homepage](https://github.com/odrobnik/codex-quota-skill) <br>
- [OpenAI Codex CLI](https://codex.openai.com) <br>
- [Setup instructions](artifact/SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local Codex session files and may write /tmp/codex-quota-all.json when checking all saved accounts.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
