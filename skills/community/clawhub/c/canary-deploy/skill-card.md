## Description: <br>
Safe system changes with automatic baseline capture, canary testing, and rollback for critical infrastructure modifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lolaopenclaw](https://clawhub.ai/user/lolaopenclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to plan and validate risky SSH, firewall, networking, systemd, kernel parameter, and service changes while preserving a rollback path. It is intended for critical system modifications where lost connectivity or failed service recovery would be costly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rollback safety may be overstated, and a captured baseline is not itself a recovery backup. <br>
Mitigation: Use a separate working access path, provide explicit --backup files, and verify that the backup files can restore the actual change before applying it. <br>
Risk: The restore path can perform privileged overwrites based on local backup metadata. <br>
Mitigation: Manually inspect the backup metadata and restore targets before rollback, especially on production or remote-only systems. <br>


## Reference(s): <br>
- [Incident Report: AllowTcpForwarding Lockout](references/incident-report.md) <br>
- [Canary Deploy release page](https://clawhub.ai/lolaopenclaw/canary-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell scripts that capture baselines, run validation commands, and restore explicit backup files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
