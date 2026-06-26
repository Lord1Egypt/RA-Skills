## Description: <br>
System health monitoring and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run local CPU, memory, disk, process, and network health checks and generate system health reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The diagnostic script reads local system state, including host, disk, network, and process details. <br>
Mitigation: Run it only on systems where that local diagnostic information is appropriate to inspect. <br>
Risk: Saved reports may contain host and process details that should not be exposed in shared, synced, or world-readable locations. <br>
Mitigation: Choose a private output path and review the report before sharing it. <br>
Risk: The network check performs a DNS lookup to google.com. <br>
Mitigation: Use the skill only when that external DNS lookup is acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eternal0404/eternal-system-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local report file when the user provides an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
