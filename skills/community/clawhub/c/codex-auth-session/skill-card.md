## Description: <br>
Refreshes Codex CLI auth.json from a local ChatGPT web session for users behind firewalls, in WSL, in containers, or on remote desktops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcz-user](https://clawhub.ai/user/zcz-user) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to refresh Codex CLI authentication from an existing local ChatGPT browser session when standard OAuth flows are blocked or unreliable, especially on Windows, WSL, containers, and remote desktop setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live ChatGPT browser session credentials and writes Codex authentication tokens to local files. <br>
Mitigation: Use only on a trusted machine or dedicated browser profile, keep browser-profile, backups, logs, and auth.json out of shared storage and backups, and revoke sessions if these files are exposed. <br>
Risk: Automatic refresh can preserve credential access beyond a single manual run. <br>
Mitigation: Review any scheduled-task setup before enabling it and disable the task when persistent refresh is no longer needed. <br>
Risk: Backups and logs may contain sensitive authentication metadata even when raw tokens are masked. <br>
Mitigation: Restrict filesystem permissions, avoid committing generated state, and delete backups and logs during incident response. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zcz-user/codex-auth-session) <br>
- [Codex CLI](https://github.com/openai/codex) <br>
- [README](references/README.md) <br>
- [Security Policy](references/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or refresh of local Codex auth files and scheduled refresh setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
