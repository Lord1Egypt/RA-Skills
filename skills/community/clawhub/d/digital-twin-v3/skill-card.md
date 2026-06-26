## Description: <br>
数字双生养成系统 v3 helps an agent establish a persistent digital-twin companion with a covenant, shared memory, value anchors, drift checks, growth dashboard, and local backup routines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejianjun000](https://clawhub.ai/user/xiejianjun000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users use this skill to set up a local digital-twin companion that records shared memories, captures value anchors, checks for response drift, and reports relationship growth. It is intended for users who want persistent personalization and are comfortable managing local companion data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and migrate personal or workspace memory data into a local companion profile. <br>
Mitigation: Review the files that may be copied before use, avoid storing secrets or highly sensitive information, and require explicit confirmation before binding or migration. <br>
Risk: Backup archives can preserve sensitive twin data and should be treated as unencrypted. <br>
Mitigation: Store backups in a protected location, delete unneeded archives, and do not share backup files unless the contents have been reviewed. <br>
Risk: Companion memory and value anchors may influence later agent behavior through persistent personalization. <br>
Mitigation: Review generated covenant, memory, and value-anchor files periodically and remove inaccurate, stale, or unsafe entries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiejianjun000/digital-twin-v3) <br>
- [Twin covenant template](artifact/templates/twin-covenant.md) <br>
- [Values anchor template](artifact/templates/values-anchor.md) <br>
- [Heartbeat checklist template](artifact/templates/heartbeat-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown files, JSON status objects, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reads local .twin memory, covenant, value-anchor, guardian-log, dashboard, prediction, and backup artifacts.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
