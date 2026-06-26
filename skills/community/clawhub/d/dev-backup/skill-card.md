## Description: <br>
Creates local project snapshots with retention, restore, list, checksums, and safer backup behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincsta](https://clawhub.ai/user/vincsta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, list, and restore local snapshots of development projects before risky changes or refactoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore can overwrite files in the target project. <br>
Mitigation: Inspect the selected snapshot first and restore only when overwriting the target project is acceptable. <br>
Risk: Retention can delete older snapshots. <br>
Mitigation: Set an explicit --keep value and use --list before backup operations when older snapshots must be preserved. <br>
Risk: The fallback copy path may include files that documentation says are excluded, including .env. <br>
Mitigation: Prefer systems with rsync available, set explicit project and output directories, and review snapshot contents before sharing or restoring. <br>
Risk: Checksum output is informational and should not be treated as restore-time verification. <br>
Mitigation: Verify important restored files independently before relying on the restored project state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincsta/dev-backup) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local filesystem snapshot output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates numbered project snapshots, maintains a .latest symlink, supports retention with --keep, and records SHA256 checksum summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
