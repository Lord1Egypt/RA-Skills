## Description: <br>
Security monitoring and alerting tool for AI agents that checks for exposed secrets, unverified skills, insecure keys, suspicious commands, and malicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suzxclaw](https://clawhub.ai/user/suzxclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to run local security checks across an OpenClaw workspace, review alerts, and identify exposed credentials, weak key permissions, unverified skills, suspicious command history, and log leaks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner inspects local secrets, logs, recent shell history, and SSH key metadata, so alert output can reveal sensitive file paths or credential context. <br>
Mitigation: Run it only in environments where local inspection is acceptable, keep generated alert logs private, and review logs for sensitive details before sharing. <br>
Risk: The server security guidance notes inconsistent Node 'bash' install metadata and asks for clearer scan path documentation. <br>
Mitigation: Review the README and permission manifest before installation, run the Bash script directly, and confirm the intended local scan paths for your workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suzxclaw/agent-security-monitor) <br>
- [README](README.md) <br>
- [Permission manifest](permissions.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Terminal output, local log files, JSON configuration, and Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes security-monitor.log and security-alerts.log in the OpenClaw workspace when run.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
