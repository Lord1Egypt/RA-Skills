## Description:

Cleans expired cache files, auto-flush files, and old logs to free disk space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to scan configured OpenClaw cache, temporary, browser, sandbox, canvas, and log directories, remove expired files, and produce a cleanup log. It can be run manually or scheduled as a recurring cron task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can schedule automatic permanent deletion every three days.

Mitigation: Review and narrow cleanup paths, add a dry-run or confirmation mode, and enable the cron schedule only after validating expected deletions.

Risk: Running the cleanup script as root can increase the impact of unintended deletions.

Mitigation: Run the script with the least-privileged account that owns the intended cache and log directories.

Risk: The cleanup log is written under /tmp, which is world-writable on many systems.

Mitigation: Move logging to a controlled application log directory with appropriate permissions before scheduled use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text cleanup log with shell command and cron configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Performs permanent file deletion based on configured directory and age rules.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
