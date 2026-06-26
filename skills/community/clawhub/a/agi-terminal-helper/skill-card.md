## Description: <br>
A practical runbook for using OpenClaw exec safely through sandbox-first exploration, explicit confirmations, and debugging playbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwujijay](https://clawhub.ai/user/liuwujijay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to guide safe terminal-command planning, execution review, sandbox use, long-running process handling, and OpenClaw troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminal guidance can lead to unsafe execution if users approve destructive commands, privileged operations, remote install scripts, or commands that expose secrets. <br>
Mitigation: Review the exact command, working directory, and affected files before approval; require explicit confirmation for destructive, privileged, remote-install, secret-handling, SSH, browser-profile, keychain, network, or system-setting changes. <br>
Risk: Host and sandbox environments may differ, especially around environment variables and permissions. <br>
Mitigation: Prefer sandboxed execution for untrusted work and verify needed environment variables, permissions, and tool availability in the actual execution context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuwujijay/agi-terminal-helper) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with example shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers terminal intent statements, working-directory selection, sandbox-first exploration, confirmation points, and OpenClaw-specific troubleshooting.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
