## Description: <br>
优雅安全的 OpenClaw 配置同步工具 - 支持选择性备份、.gitignore 规则、版本控制 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to back up, restore, and selectively synchronize OpenClaw workspace configuration, memories, and custom skills to a remote Git repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive OpenClaw workspace data to a remote Git repository. <br>
Mitigation: Use only a private dedicated repository, add explicit ignore rules for secrets, and inspect selected directories before syncing. <br>
Risk: The backup token is stored in ~/.openclaw/.backup.env and may grant remote repository access. <br>
Mitigation: Create a fine-grained least-privilege token and restrict permissions on ~/.openclaw/.backup.env. <br>
Risk: The sync behavior can force-push to the configured remote branch. <br>
Mitigation: Run --dry-run first and confirm the target repository, branch, and instance ID before executing a sync. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/russellfei/elegant-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
