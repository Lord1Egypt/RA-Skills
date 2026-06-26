## Description: <br>
Automated disk space cleanup and maintenance for OpenClaw deployments across SQLite files, Docker resources, logs, temporary files, package caches, git workspaces, and stale migration artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yagebin79386](https://clawhub.ai/user/yagebin79386) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to recover disk space and maintain OpenClaw deployments when storage usage grows after long-running service operation, sandbox rebuilds, package installs, or reindexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete broad host and workspace data. <br>
Mitigation: Install only on a dedicated OpenClaw machine, run --dry-run first, and review every path and Docker cleanup effect before live execution. <br>
Risk: The skill can make persistent system logging changes by limiting journald retention. <br>
Mitigation: Confirm the host logging policy before live runs and avoid unattended aggressive cron mode until the cleanup scope has been reviewed. <br>
Risk: The skill may remove old workspace virtual environments and other stale artifacts. <br>
Mitigation: Set OPENCLAW_HOME and OPENCLAW_WORKSPACE deliberately, review dry-run output, and keep recoverable backups for workspaces that may contain needed local state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yagebin79386/disk-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline bash commands and terminal output strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The cleanup script supports dry-run, normal, aggressive, and quiet modes and ends with a machine-parseable CLEAN or CLEANED summary line.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
