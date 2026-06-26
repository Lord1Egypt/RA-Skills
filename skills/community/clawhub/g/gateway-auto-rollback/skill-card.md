## Description: <br>
Automatically backs up, validates, and rolls back OpenClaw Gateway configuration files when changes fail JSON validation or gateway health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to protect OpenClaw Gateway configuration changes with local backups, JSON validation, gateway health checks, and rollback commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify and restore critical OpenClaw configuration files, command approvals, and the skills registry. <br>
Mitigation: Test it on a non-critical profile first, inspect proposed changes and backups before restoring, and confirm the restored configuration is appropriate for the active environment. <br>
Risk: Watch or cron mode should not be treated as a complete pre-change safety net because rollback guarantees are unreliable. <br>
Mitigation: Use manual pre-change backups for important edits, verify Gateway health after changes, and avoid relying on background monitoring alone for production recovery. <br>
Risk: Backups under ~/.openclaw/backup may preserve sensitive or outdated permission state. <br>
Mitigation: Protect the backup directory with appropriate local access controls and periodically prune backups that are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/.openclaw and requires Python 3.8+ with OpenClaw Gateway available for health checks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
