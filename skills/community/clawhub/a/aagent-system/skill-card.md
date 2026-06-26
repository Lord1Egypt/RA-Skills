## Description: <br>
Aagent System is a multi-agent automation system for AI agent skill sample collection, security scanning, threat intelligence collection, and detection rule iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security researchers use this skill to run a local multi-agent crawler and scanner for collecting AI agent skill samples, detecting potentially malicious packages, extracting indicators, and updating research data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-running local worker processes can consume CPU, memory, process slots, disk space, and outbound registry bandwidth. <br>
Mitigation: Run in an isolated workspace, monitor CPU, memory, outbound traffic, process count, and generated data files, and stop the manager when collection is not needed. <br>
Risk: The security scan summary says the skill runs undeclared local shell scripts from referenced home-directory paths. <br>
Mitigation: Review or remove the referenced ~/aass-* scripts before running and install only when those scripts are expected in the target environment. <br>
Risk: Large-scale sample collection can store high volumes of package and scan metadata locally. <br>
Mitigation: Set collection limits appropriate for the environment and periodically inspect or rotate the generated JSON data files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caidongyun/aagent-system) <br>
- [Publisher profile](https://clawhub.ai/user/caidongyun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown instructions with slash commands, shell commands, and JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts and manages local worker processes that write sample, scan, malicious finding, performance, and evolution data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
