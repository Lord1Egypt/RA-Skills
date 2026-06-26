## Description: <br>
Backs up personalized OpenClaw configuration and user data to a GitHub repository with dry-run preview and restore support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangbb-coder](https://clawhub.ai/user/fangbb-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to back up personalized configuration, memory, identity, task, and custom script files to a GitHub repository, then restore them onto a fresh installation when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can upload sensitive OpenClaw memory, identity, profile, configuration, and optional credential files to GitHub. <br>
Mitigation: Use a private repository, set a fine-grained token limited to that repository, run dry-run first, review the file list, and exclude credentials unless they are encrypted. <br>
Risk: Restore can overwrite existing OpenClaw memory and configuration. <br>
Mitigation: Treat restore as a high-impact operation, confirm the target repository and latest backup before restoring, and keep a separate local copy of current files before proceeding. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports backup, restore, and dry-run workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
