## Description: <br>
Clawon helps users back up and restore an OpenClaw workspace, including memory, skills, configuration, and optional local or cloud snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chelouche9](https://clawhub.ai/user/chelouche9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use Clawon to preview, back up, restore, and schedule local or cloud snapshots of workspace files, skills, memory, configuration, and optional session or secret data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain sensitive workspace data when users opt into memory databases, sessions, or secrets. <br>
Mitigation: Run discovery and secret scanning before backup, keep sensitive options opt-in, and use encryption for backups that include secrets or are uploaded to cloud storage. <br>
Risk: Cloud backup and restore require a Clawon account and API key, which can be exposed if handled inline in shell commands. <br>
Mitigation: Verify the npm package or use a reviewed local clone, prefer the CLAWON_API_KEY environment variable, and rotate any key that may have been exposed. <br>
Risk: Scheduled backups create a persistent cron entry on supported systems. <br>
Mitigation: Enable scheduling only when persistent backups are intended, review schedules with status or crontab inspection, and disable schedules when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chelouche9/clawon) <br>
- [Clawon homepage](https://clawon.io) <br>
- [Clawon CLI repository](https://github.com/chelouche9/clawon-cli) <br>
- [Clawon npm package](https://www.npmjs.com/package/clawon) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance should start with discovery before backup or restore actions and should keep API keys and encryption passphrases under user control.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
