## Description: <br>
Bootstrap, repair, and verify the ClawMem OpenClaw plugin when it is not installed, not active, missing per-agent provisioning, or needs setup troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianthereal](https://clawhub.ai/user/ianthereal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, activate, verify, and repair ClawMem as the active OpenClaw memory plugin. After setup, it directs agents to use the bundled runtime ClawMem skill for everyday memory operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup commands change the active OpenClaw memory plugin configuration and may restart the gateway. <br>
Mitigation: Review commands before execution, validate configuration, and warn before restart when it may interrupt an active response stream. <br>
Risk: Verification steps read per-agent route details and tokens that could expose credentials if logs or screenshots are shared. <br>
Mitigation: Protect the OpenClaw configuration and ClawMem token, and avoid sharing logs or screenshots that may contain credentials. <br>
Risk: The install flow retrieves an external plugin package. <br>
Mitigation: Pin or verify the external plugin package source when the environment supports it. <br>


## Reference(s): <br>
- [ClawMem ClawHub listing](https://clawhub.ai/ianthereal/clawmem) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell, Python, text, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, verification commands, optional compatibility snippets, and repair checklists.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
