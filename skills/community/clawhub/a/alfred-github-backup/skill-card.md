## Description: <br>
Backs up an OpenClaw workspace to a private GitHub repository with guided setup, manual backup, restore, status checks, and scheduled backup support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziqi-jin](https://clawhub.ai/user/ziqi-jin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure private GitHub backups for workspace files, run manual backups, inspect backup status, and restore from a repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles GitHub tokens during setup and backup operations. <br>
Mitigation: Use a fine-grained, revocable GitHub token limited to one private backup repository, and avoid pasting tokens into chat. <br>
Risk: The backup workflow can commit workspace memory, identity, and configuration files that may contain private data. <br>
Mitigation: Inspect exactly what will be committed before pushing, and exclude or encrypt memory and identity files if they contain private data. <br>
Risk: Scheduled backups may continue pushing sensitive changes after initial setup. <br>
Mitigation: Confirm how to list, disable, or remove the scheduled backup before enabling automated runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziqi-jin/alfred-github-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and interactive setup prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational backup and restore instructions; may also invoke or propose Git and OpenClaw cron commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
