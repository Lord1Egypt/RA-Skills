## Description: <br>
Cleans expired cache files, auto-flush files, and old logs to free disk space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to remove stale local cache, temporary files, sandbox, browser, canvas, and log files, either manually or on a recurring cron schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script deletes old local OpenClaw cache, logs, browser, canvas, sandbox, cron temporary files, OpenClaw-named /tmp files, and project .cache directories. <br>
Mitigation: Install only when those locations are safe to clean, review the hard-coded /root/.openclaw path, and add dry-run behavior or exclusions for files that must be retained. <br>
Risk: The bundled cron schedule can run cleanup automatically before each affected location has been reviewed. <br>
Mitigation: Disable or adjust the cron schedule until retention requirements and target paths are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/cache-cleanup) <br>
- [Publisher profile](https://clawhub.ai/user/xaiohuangningde) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Shell script execution with a plain-text cleanup log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a dated log under /tmp and deletes matching expired files from configured local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
