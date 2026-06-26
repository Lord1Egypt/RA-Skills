## Description: <br>
Cron Sentinel helps agents wrap scheduled commands so each run is recorded, retried when configured, and checked for failed or overdue executions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to monitor recurring cron or scheduled jobs by wrapping commands, recording recent run state, and surfacing loud failures or silent missed runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wrapped commands run through the local shell and can perform whatever action the provided command performs. <br>
Mitigation: Use the skill only for commands the user explicitly chooses and review generated shell or crontab commands before running them. <br>
Risk: Recent command output is recorded locally and may include secrets if the wrapped job prints credentials or tokens. <br>
Mitigation: Avoid wrapping commands that print secrets, redirect sensitive output away from Sentinel, and protect the state file location. <br>
Risk: Command output shown in logs or status views may be unsafe to inspect if the wrapped command is untrusted. <br>
Mitigation: Avoid untrusted wrapped commands or review logs in a safe viewer until output sanitization is added. <br>


## Reference(s): <br>
- [Cron Sentinel ClawHub release page](https://clawhub.ai/chris-openclaw/cron-sentinel) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include crontab entries, watchdog commands, status interpretation, and retry or timeout settings.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
