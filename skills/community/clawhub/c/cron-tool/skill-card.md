## Description: <br>
Perform cron-tool operations from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage user cron jobs from the command line, including adding, disabling, backing up, restoring, and editing scheduled commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron changes persist and scheduled commands continue running after they are added or restored. <br>
Mitigation: Back up the current crontab first and only add or restore commands that have been reviewed. <br>
Risk: The security summary reports that removing a job by numeric line number may wipe the whole crontab. <br>
Mitigation: Avoid numeric --remove until the issue is fixed; verify the current crontab and maintain a backup before removing jobs. <br>
Risk: Restoring from a file replaces the current crontab. <br>
Mitigation: Inspect the restore file and the current crontab before confirming the replacement. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dinghaibin/cron-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May affect the current user's crontab when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
