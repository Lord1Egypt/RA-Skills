## Description: <br>
Doc Sysadmin helps agents check and maintain Ubuntu 24.04 host health, including disk space, memory, slowdowns, and periodic cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zelzaclaw](https://clawhub.ai/user/zelzaclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and technical users can use this skill to guide Ubuntu 24.04 system health checks, review disk and memory pressure, investigate slowdowns, and propose cleanup commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled cleanup script can perform broad system changes, including automatic package removal, deletion of temporary directories, journal vacuuming, and cache dropping. <br>
Mitigation: Review commands before use, prefer a dry run or explicit confirmation flow, and run only the specific maintenance steps that are intended for the current host. <br>
Risk: The cleanup behavior may delete temporary data without matching the skill's narrower safe-cleanup guidance. <br>
Mitigation: Restrict temp cleanup to clearly scoped old files and avoid running scripts/cleanup.sh as-is on a real Ubuntu system. <br>


## Reference(s): <br>
- [Doc Sysadmin on ClawHub](https://clawhub.ai/zelzaclaw/doc-sysadmin) <br>
- [Ubuntu 24.04 Essential Commands](references/ubuntu24-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose privileged Ubuntu maintenance commands that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
