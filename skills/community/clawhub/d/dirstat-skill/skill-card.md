## Description:

Use when auditing disk usage on Windows or Linux and suggesting what a human should review to reclaim space without changing files automatically, especially for caches, model files, trash, and partial downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jagones84](https://clawhub.ai/user/jagones84)

### License/Terms of Use:

Apache License 2.0

## Use Case:

Developers, operators, and agents use this skill to audit explicit Windows or Linux filesystem paths, generate compact disk-usage reports, and identify review candidates for human space-recovery decisions without changing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw disk-audit exports and reports may contain sensitive local path names.

Mitigation: Prefer narrow scan paths over whole-drive scans unless full-machine metadata capture is intended, and handle generated reports as local sensitive data.

Risk: The read-only workflow includes a Linux helper installer that can take a sudo password from stdin.

Mitigation: Install ncdu manually or review scripts/linux/install_ncdu.sh before use, and do not pipe sudo passwords into helper scripts.

Risk: Disk-usage findings can be mistaken for cleanup instructions.

Mitigation: Treat all candidates as review prompts only; the skill should not emit cleanup commands or change files automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jagones84/skills/dirstat-skill)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [Examples README](examples/README.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, CSV files, JSON data, shell commands, and concise human-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit outputs may include raw exports and reports containing local file path metadata.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
