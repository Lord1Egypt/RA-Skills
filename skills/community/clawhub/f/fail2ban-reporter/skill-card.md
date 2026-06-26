## Description: <br>
Reports fail2ban-banned IPs to AbuseIPDB and provides shell commands for checking IP reputation, viewing stats, and installing auto-reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jestersimpps](https://clawhub.ai/user/jestersimpps) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and server operators use this skill to report fail2ban SSH bans to AbuseIPDB, check the reputation of specific IPs, and review ban and reporting statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing auto-reporting gives the skill persistent privileged access to fail2ban configuration. <br>
Mitigation: Install only on servers where automatic reporting is intended, and review the scripts before running sudo install. <br>
Risk: The reporting scripts share banned IP addresses and comments with AbuseIPDB under the user's API key. <br>
Mitigation: Confirm that third-party sharing of banned IPs and report comments is acceptable for the environment before enabling reporting. <br>
Risk: Telegram alerts are described by the skill summary, but the security guidance says not to depend on them unless an implementation is added. <br>
Mitigation: Treat Telegram notifications as unavailable until the implementation exists and has been reviewed. <br>


## Reference(s): <br>
- [AbuseIPDB API Reference](references/abuseipdb-api.md) <br>
- [AbuseIPDB API](https://api.abuseipdb.com/api/v2) <br>
- [Clawdbot](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install fail2ban action configuration and write AbuseIPDB report status to /var/log/abuseipdb-reports.log when the user runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
