## Description:

ClawHub Smart Updater helps agents check installed ClawHub skills for updates, back up local copies, identify conflicts, and produce merge reports before changes are applied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vilda007](https://clawhub.ai/user/vilda007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep locally installed ClawHub skills current while preserving local modifications. It is most useful when users want dry-run review, backups, diff reports, and manual review for conflicting updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the updater can automatically rewrite installed skills and may overstate safety claims.

Mitigation: Run manually in dry-run mode first, review proposed changes to skill files and dependencies, and avoid unattended scheduled use until the documented safeguards are verified.

Risk: The security guidance calls out unsafe validation and shell command execution concerns.

Mitigation: Avoid using --force, review generated diffs before accepting updates, and prefer manual approval for code or dependency changes.

Risk: Automatic safe updates can still alter local SKILL.md, JSON, script, or dependency files in ways the user did not intend.

Mitigation: Keep backups enabled, inspect the generated update report, and restore or manually merge when changes affect important local customizations.

## Reference(s):

- [ClawHub Smart Updater release page](https://clawhub.ai/vilda007/skills/clawhub-smart-updater)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [VETTING_REPORT.md](artifact/VETTING_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal status text, diff files, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write backup folders, temporary downloaded skill files, diff reports, and dated update reports in the configured workspace.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
