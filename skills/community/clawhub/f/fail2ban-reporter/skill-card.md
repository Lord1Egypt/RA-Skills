## Description:

Auto-reports fail2ban banned IPs to AbuseIPDB, supports IP reputation checks, and summarizes fail2ban and reporting activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jestersimpps](https://clawhub.ai/user/jestersimpps)

### License/Terms of Use:


## Use Case:

Developers and server operators use this skill to report fail2ban-blocked SSH attackers to AbuseIPDB, check IP reputation, and review ban/report statistics. It is intended for systems where operators are comfortable granting scripts access to fail2ban, system configuration, logs, and AbuseIPDB API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The privileged installer changes fail2ban configuration, restarts fail2ban, and requires root-level access.

Mitigation: Review the scripts before installing, back up fail2ban configuration, and install only on systems where root-level configuration changes are acceptable.

Risk: The security evidence reports a command-injection risk in the persistent installer when run from an untrusted or strangely named directory.

Mitigation: Do not run install.sh from an untrusted or strangely named directory until the action path is safely fixed.

Risk: The skill automatically sends banned IP addresses and report comments to AbuseIPDB.

Mitigation: Confirm that sharing banned IP data and comments with AbuseIPDB is acceptable for the deployment environment before enabling auto-reporting.

## Reference(s):

- [AbuseIPDB API Reference](references/abuseipdb-api.md)
- [fail2ban Reporter ClawHub Release](https://clawhub.ai/jestersimpps/skills/fail2ban-reporter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON excerpts from AbuseIPDB responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install or remove fail2ban action configuration and may write reporting status to /var/log/abuseipdb-reports.log when scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
