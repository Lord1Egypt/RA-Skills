## Description: <br>
Manage persistent local OpenClaw secrets safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up, inspect, validate, and troubleshoot persistent local OpenClaw secrets or environment variables without exposing secret values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret values could be exposed through chat, logs, diagnostics, screenshots, memory files, or final reports. <br>
Mitigation: Report only key names, paths, presence or absence, permissions, and validation results; redact values and never copy tokens, passwords, private keys, or full environment contents. <br>
Risk: Changing credential mechanisms, secret paths, permissions, or restarting the OpenClaw gateway could interrupt active work or weaken local secret handling. <br>
Mitigation: Ask before changing credential mechanisms, paths, permissions policy, or restarting active services; apply changes additively and validate feature behavior after approved reloads or restarts. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/daniel-refahi-ikara/skills/dr-agent-secrets) <br>
- [Publisher profile](https://clawhub.ai/user/daniel-refahi-ikara) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only procedure; outputs should redact secret values and report paths, permissions, reload or restart status, validation results, and remaining approvals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
