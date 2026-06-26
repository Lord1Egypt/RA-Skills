## Description: <br>
Claw Self Evolution installs OpenClaw maintenance scripts for learning logs, scheduled checks, backups, directory validation, isolated experiments, and approval-based self-improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenz1117](https://clawhub.ai/user/kenz1117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add maintenance automation to an OpenClaw workspace, including health checks, backups, learning records, directory cleanup, and isolated self-improvement workflows that require approval before merging changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled jobs can automatically change workspace files and user memory. <br>
Mitigation: Review and edit every scheduled job before enabling it, and disable or rewrite the automatic user-profile updater unless the behavior is explicitly desired. <br>
Risk: Directory repair and cleanup scripts may move, merge, or delete files without enough user control. <br>
Mitigation: Add dry-run or confirmation gates before enabling directory repair or cleanup automation. <br>
Risk: Service health checks can restart services automatically. <br>
Mitigation: Avoid enabling auto-restart until the target service, logs, and rollback behavior are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenz1117/claw-self-evolution) <br>
- [Publisher profile](https://clawhub.ai/user/kenz1117) <br>
- [self-improving-agent inspiration](https://github.com/pskoett/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with bash, JSON configuration examples, and Python maintenance scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates workspace files when installed or scheduled; review job definitions before enabling automation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
