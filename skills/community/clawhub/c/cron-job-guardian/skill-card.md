## Description:

Audits cron or timer configurations for frequency, idempotency, retry, logging, and concurrency risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to review cron files, timer definitions, script directories, or task descriptions and receive structured findings before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Directory scans may unintentionally read through symlinks outside the selected folder.

Mitigation: Use the skill only on directories you control and check for symlinks before scanning untrusted folders or repositories.

Risk: The --output option writes a local file and could overwrite or create files in an unintended location.

Mitigation: Prefer stdout or dry-run during review, and choose output paths deliberately when writing reports.

## Reference(s):

- [Cron Job Guardian ClawHub page](https://clawhub.ai/52yuanchangxing/skills/cron-job-guardian)
- [README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance, configuration]

**Output Format:** [Markdown or JSON structured audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local output file when --output is used; otherwise emits to stdout.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
