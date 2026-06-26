## Description: <br>
Helps answer OpenClaw questions, troubleshoot configuration and runtime issues, and propose OpenClaw CLI commands for fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thincher](https://clawhub.ai/user/Thincher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer OpenClaw usage, configuration, and troubleshooting questions, consult local OpenClaw documentation, and prepare CLI-based remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest OpenClaw configuration changes through `openclaw config set`. <br>
Mitigation: Review each proposed configuration change before execution. <br>
Risk: The skill may update local troubleshooting notes or documentation indexes. <br>
Mitigation: Only save verified fixes, and do not store tokens, passwords, private logs, or unverified guidance in notes. <br>


## Reference(s): <br>
- [Experience notes](references/experience.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose OpenClaw CLI commands and updates to local troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
