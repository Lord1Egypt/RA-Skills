## Description: <br>
Clawpilot helps agents install, configure, harden, troubleshoot, and audit OpenClaw self-hosted AI gateway deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason513597](https://clawhub.ai/user/jason513597) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to guide OpenClaw setup, channel configuration, security hardening, local audits, prompt and transcript inspection, multi-agent routing, and cloud deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run local or network checks and inspect sensitive OpenClaw configuration, prompts, and session data. <br>
Mitigation: Approve update checks, config scans, prompt scans, and transcript scans deliberately; review findings before acting on them. <br>
Risk: Audit output can include secrets, private chat content, or internal paths. <br>
Mitigation: Avoid sharing raw audit output and redact sensitive values before using results outside the local environment. <br>
Risk: The release is from a third-party publisher. <br>
Mitigation: Install only if you trust the publisher and verify the bundled scripts before execution. <br>


## Reference(s): <br>
- [Clawpilot ClawHub listing](https://clawhub.ai/jason513597/clawpilot) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Security Hardening](references/security.md) <br>
- [Cloud Deployment](references/cloud-deployment.md) <br>
- [Multi-Agent Routing](references/multi-agent.md) <br>
- [OpenClaw docs index](https://docs.openclaw.ai/llms.txt) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local audit, configuration, prompt, and transcript scan commands for user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
