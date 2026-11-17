## Description:

Checks installed skills for publisher updates, summarizes changes, and supports backed-up updates and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Skill users and developers check installed skills for newer publisher releases and review changes before choosing whether to update or roll back.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A default check creates tracking files in installed skill directories, despite being described as read-only.

Mitigation: Use check --no-baseline for inspection without creating tracking files; review this behavior before installation if read-only operation is required.

Risk: Opt-in update options can modify installed skills, including major upgrades or locally modified files.

Mitigation: Review proposed changes and backups before using --execute, autoupdate --on, --allow-major, or --force-overwrite.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/j-levee/skills/cjg-skill-sync)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Plain-text update reports and commands; JSON for version-gate decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.3.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
