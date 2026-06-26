## Description: <br>
Agent Security Framework for OpenClaw provides Docker containerization guidance, fake-agent detection, security scanning, and hardening guidance for AI agent deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffvsutherland](https://clawhub.ai/user/jeffvsutherland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to assess and harden OpenClaw agent deployments, including container isolation, security scanning, fake-agent detection, and operational security controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes broad autonomous work-claiming, board-polling, status-posting, and persistence instructions beyond a normal security-hardening workflow. <br>
Mitigation: Review SOUL.md before installation and remove or gate Mission Control, channel announcement, heartbeat, story-claiming, and memory-update instructions when only security scanning or hardening guidance is needed. <br>
Risk: Some workflows may involve sensitive credentials or security controls for agent deployments. <br>
Mitigation: Run commands in a controlled environment, avoid sharing secrets in chat or logs, and require human review before applying firewall, authentication, network egress, or deployment changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffvsutherland/agent-security-framework) <br>
- [SECURITY-HARDENING.md](artifact/SECURITY-HARDENING.md) <br>
- [SOUL.md](artifact/SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose security checks, hardening steps, container settings, and operational coordination actions for OpenClaw deployments.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
