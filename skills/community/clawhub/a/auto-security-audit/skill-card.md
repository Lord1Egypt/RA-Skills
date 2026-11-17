## Description:

Auto Security Audit runs nmap, nuclei, sslscan, SSH, firewall, fail2ban, patch, and login checks to generate Markdown security reports and notification-ready summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nashbuaa-ops](https://clawhub.ai/user/nashbuaa-ops)

### License/Terms of Use:


## Use Case:

Developers, operators, and security engineers use this skill to run authorized host security checks and produce structured reports covering exposed services, known vulnerabilities, TLS posture, SSH configuration, firewall state, fail2ban status, available updates, and recent logins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install a mutable nuclei release system-wide.

Mitigation: Pin the nuclei version and verify the downloaded artifact with an expected checksum or signature before installation.

Risk: The generated reports may contain sensitive host, service, vulnerability, and login details.

Mitigation: Store reports in a restricted location, limit sharing of notification summaries, and treat report contents as sensitive security data.

Risk: Port and vulnerability scanning can affect systems or networks outside the user's authority.

Mitigation: Run scans only against owned or explicitly authorized systems and public IP addresses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nashbuaa-ops/skills/auto-security-audit)
- [ProjectDiscovery nuclei latest release API](https://api.github.com/repos/projectdiscovery/nuclei/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal summary text and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written under ~/.openclaw/workspace/reports and include a latest-scan-summary.txt file for scheduled notification workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
