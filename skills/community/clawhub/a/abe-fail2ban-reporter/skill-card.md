## Description:

Auto-reports fail2ban banned IPs via SkillBoss API Hub, supports manual IP reputation checks and ban stats, and can send alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server operators use this skill to inspect fail2ban bans, report or look up banned IPs through SkillBoss API Hub, and optionally enable automatic reporting from fail2ban actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer creates a persistent root-level fail2ban hook that runs reporting code from the skill directory.

Mitigation: Review and back up fail2ban configuration before installation, and deploy the reporting script to a root-owned, non-writable path before enabling the action.

Risk: The reporting workflow sends banned IPs and incident comments to an external SkillBoss/HeyBoss API.

Mitigation: Confirm that this external data flow is approved for the environment before running reporting or auto-reporting scripts.

## Reference(s):

- [SkillBoss API Hub Reference](references/skillboss-api.md)
- [API Reference (SkillBoss API Hub)](references/abuseipdb-api.md)
- [Skill release page](https://clawhub.ai/abeltennyson/skills/abe-fail2ban-reporter)
- [Publisher profile](https://clawhub.ai/user/abeltennyson)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and shell script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write fail2ban configuration and local log entries when installation or reporting scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
