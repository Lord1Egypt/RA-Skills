## Description:

Audits household backups against the 3-2-1 rule, estimates ransomware exposure, and suggests affordable redundancy and restore-test steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Households and individuals use this skill to inventory important data, identify fragile or ransomware-exposed backups, plan additional copies, and schedule restore tests. It is not intended for enterprise backup policy or active incident response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local backup inventory and restore-test notes may reveal sensitive asset names and locations.

Mitigation: Use generic asset labels when appropriate and protect or delete the local registry after use.

Risk: A backup classification or passing audit may not reflect whether files can actually be restored.

Mitigation: Confirm copy locations and versioning, then periodically restore and open sample files.

## Reference(s):

- [Backup 3-2-1 Auditor strategy guide](references/strategy-guide.md)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/backup-3-2-1-auditor)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text audit reports, recovery estimates, redundancy plans, and restore-test prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asset inventory and restore-test notes are saved locally in backup-registry.json.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
