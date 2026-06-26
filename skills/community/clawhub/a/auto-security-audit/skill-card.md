## Description: <br>
Automates authorized security audits with nmap port and vulnerability scans, nuclei web vulnerability checks, SSL/TLS review, SSH/firewall/fail2ban checks, patch and login review, and Markdown report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nashbuaa-ops](https://clawhub.ai/user/nashbuaa-ops) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and system operators use this skill to run authorized host security scans and generate structured findings for review, scheduled follow-up, or Feishu/Lark notification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running security scans against systems without permission can be unauthorized activity. <br>
Mitigation: Install and run the skill only on systems you own or are explicitly authorized to test. <br>
Risk: The installation workflow downloads nuclei before moving it into /usr/local/bin. <br>
Mitigation: Verify the nuclei download and release source before installing it on the host. <br>
Risk: Generated reports may contain sensitive host, service, vulnerability, patch, and login information. <br>
Mitigation: Restrict access to reports under the OpenClaw workspace and handle summaries as sensitive security data. <br>
Risk: Scheduled scans and Feishu/Lark notifications can repeatedly execute scans or send findings outside the host. <br>
Mitigation: Enable cron and notification delivery only when recurring scans and external summary delivery are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nashbuaa-ops/auto-security-audit) <br>
- [ProjectDiscovery nuclei releases](https://github.com/projectdiscovery/nuclei/releases/latest) <br>
- [ProjectDiscovery nuclei release API](https://api.github.com/repos/projectdiscovery/nuclei/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal status output, Markdown security report, and plain-text latest scan summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates dated reports and latest-scan-summary.txt under ~/.openclaw/workspace/reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
