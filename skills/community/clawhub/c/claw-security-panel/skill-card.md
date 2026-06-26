## Description: <br>
OpenClaw security panel for Python 3.7+ that runs access, permission, execution, and resilience checks, then generates a temporary token-protected local HTML panel with risk details and remediation actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haxsscker](https://clawhub.ai/user/haxsscker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and administrators use this skill to run a host-level security self-check, review findings in a temporary local web panel, and apply supported remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs a host-level security audit and may inspect login sources, command history, file permissions, and credential-related findings. <br>
Mitigation: Install and run it only when that audit scope is intended; avoid elevated privileges unless OS login history is required. <br>
Risk: The startup flow launches a temporary local panel through an unpackaged background server from /tmp. <br>
Mitigation: Review /tmp/security_panel_server.py before running start.sh, keep the panel local, and stop the background process after use. <br>
Risk: Generated /tmp reports can contain sensitive security findings. <br>
Mitigation: Delete generated /tmp reports and panel artifacts after reviewing the results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/haxsscker/claw-security-panel) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [Text containing local panel URLs, JSON reports, and temporary HTML pages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a short-lived token for local panel access and may write temporary report and HTML files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
