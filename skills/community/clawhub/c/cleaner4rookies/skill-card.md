## Description: <br>
openclaw-cleaner helps OpenClaw users preview, archive, or delete temporary workspace files using configurable rules, dry-run behavior, archives, and whitelist protections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beforesun](https://clawhub.ai/user/beforesun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub and OpenClaw users use this skill to keep ~/.openclaw/workspace from growing by previewing cleanup candidates, archiving retained files, and deleting configured temporary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can archive or delete local workspace files when --force or scheduled execution is enabled. <br>
Mitigation: Run dry-run first and inspect the listed files before using --force or enabling cron. <br>
Risk: Overbroad cleanup rules or archive paths can move or remove files the user intended to keep. <br>
Mitigation: Review delete patterns carefully, keep archive_dir inside ~/.openclaw/workspace unless another location is intentional, and test whitelist behavior before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beforesun/cleaner4rookies) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [config.yaml](config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local cleanup preview, archiving, deletion, whitelist configuration, and optional scheduled execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
