## Description: <br>
Self-healing stability monitor for AI agents - 5 core checks + 15 extended checks, auto-recovery, health scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor AI agent and host stability, inspect service health, calculate health scores, and initiate configured recovery actions when sessions, services, memory, disk, or context checks fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically kill sessions, restart services, and compact context when recovery actions are invoked. <br>
Mitigation: Run `status` or `check` before `heal`, review the source and configuration, and validate thresholds and whitelists before enabling unattended recovery on production systems. <br>
Risk: The skill inspects broad host state and full mode can make external network probes. <br>
Mitigation: Use standard checks unless full diagnostics are required, review configured targets, and confirm that external probes are acceptable for the deployment environment. <br>
Risk: The server security verdict is suspicious despite no specific risk findings. <br>
Mitigation: Treat the skill as requiring additional review before deployment and follow the server guidance for source review and staged execution. <br>


## Reference(s): <br>
- [Aegis Protocol ClawHub listing](https://clawhub.ai/ankechenlab-node/aegis-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented status output with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration and log files when invoked for initialization, checks, or recovery.] <br>

## Skill Version(s): <br>
0.12.9 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
