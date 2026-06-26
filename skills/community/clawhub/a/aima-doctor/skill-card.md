## Description: <br>
Diagnose and repair OpenClaw when your agent is stuck, confused, or failing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyguan92](https://clawhub.ai/user/skyguan92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose process health, repair configuration issues, and recover AIMA device registration or token state when normal agent workflows are degraded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run an external local repair helper with broad authority over OpenClaw configuration and recovery state. <br>
Mitigation: Install only when the publisher is trusted, verify the published checksum before execution, and review the helper scripts where practical. <br>
Risk: Repair workflows may touch sensitive device registration, token recovery, or local configuration state. <br>
Mitigation: Run in a constrained or disposable environment for sensitive installations and avoid sharing tokens or recovery codes in chat. <br>


## Reference(s): <br>
- [AIMA Doctor homepage](https://aimaservice.ai/doctor) <br>
- [AIMA OpenClaw repository](https://github.com/Approaching-AI/aima-openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/skyguan92/aima-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May relay questions or results from the local AIMA Doctor helper and should avoid exposing sensitive tokens or recovery codes.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
