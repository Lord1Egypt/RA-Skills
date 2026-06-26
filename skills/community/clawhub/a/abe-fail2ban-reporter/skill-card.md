## Description: <br>
Auto-report fail2ban banned IPs via SkillBoss API Hub and notify via Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Server administrators and security engineers use this skill to inspect fail2ban bans, report banned IPs to SkillBoss API Hub, install or remove auto-reporting, and review reporting stats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation applies automatic fail2ban configuration changes and can restart fail2ban on the host. <br>
Mitigation: Review scripts/install.sh first, run it only on servers where auto-reporting is intended, and back up /etc/fail2ban/jail.local before installation. <br>
Risk: New fail2ban ban events can continue generating outbound API calls to SkillBoss API Hub until auto-reporting is removed. <br>
Mitigation: Confirm the API key scope and operational intent before installation, monitor /var/log/skillboss-ip-reports.log, and run scripts/uninstall.sh to stop automatic reporting. <br>
Risk: The skill requires the sensitive SKILLBOSS_API_KEY credential. <br>
Mitigation: Provide the key only in the intended server environment and avoid exposing it in logs, shell history, or shared configuration. <br>


## Reference(s): <br>
- [SkillBoss API Hub Reference](references/skillboss-api.md) <br>
- [API Reference (SkillBoss API Hub)](references/abuseipdb-api.md) <br>
- [ClawHub release page](https://clawhub.ai/abeltennyson/abe-fail2ban-reporter) <br>
- [Clawdbot project](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that may call SkillBoss API Hub, query fail2ban, modify fail2ban configuration, and write local report logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
