## Description:

Migrate settings from EasyClaw into OpenClaw by locating EasyClaw desktop and runtime configuration files, comparing them with ~/.openclaw/openclaw.json, and generating a backup-aware selective merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjingh](https://clawhub.ai/user/sjingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect EasyClaw configuration sources, identify settings with OpenClaw equivalents, and perform a selective, backup-aware migration into ~/.openclaw/openclaw.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway tokens can appear in merge output or dry-run logs.

Mitigation: Review or patch the merge script so token values are redacted before running it, avoid sharing logs, and rotate any token that may already have been exposed.

Risk: Applying the migration modifies OpenClaw configuration and creates additional plaintext backup files.

Mitigation: Run a dry run first, review planned changes, create backups with owner-only permissions, and confirm backup storage is acceptable before using --apply.

## Reference(s):

- [Migration Mapping](references/mapping.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local EasyClaw and OpenClaw JSON configuration files and, with --apply, update ~/.openclaw/openclaw.json after writing a backup.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
