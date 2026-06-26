## Description: <br>
Automatically updates OpenClaw and installed skills on a configurable schedule, handling package manager detection, local changes, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayao99315](https://clawhub.ai/user/ayao99315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep OpenClaw and installed ClawHub skills updated, either manually or through a scheduled cron job. It helps configure update schedules, skip lists, pre-release filtering, gateway restarts, notifications, and dry-run checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended updates can persistently change OpenClaw and installed skills. <br>
Mitigation: Run the dry-run mode before enabling scheduled execution, inspect the cron entry, and review update logs after changes. <br>
Risk: Automatic skill updates may affect sensitive, customized, or locally modified skills. <br>
Mitigation: Keep sensitive or customized skills in the skipSkills list and rely on the local-change checks before allowing updates. <br>
Risk: Notifications may send update status to an unintended destination. <br>
Mitigation: Disable notifications or set notifyTarget only to a trusted destination. <br>
Risk: Configuration or schedule mistakes can cause updates to run at the wrong time or with the wrong behavior. <br>
Mitigation: Validate the config file, cron schedule, and skipPreRelease setting before enabling automatic runs. <br>


## Reference(s): <br>
- [Config Schema](references/config-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ayao99315/ayao-updater) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce cron setup instructions, dry-run guidance, update summaries, notification guidance, and log inspection commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
