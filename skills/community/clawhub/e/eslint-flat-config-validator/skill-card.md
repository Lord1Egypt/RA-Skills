## Description:

Validate ESLint v9+ flat config files (JSON-exported) for structural correctness, language options, rules configuration, plugin hygiene, file patterns, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit ESLint v9+ flat configuration snapshots, review eslint.config.js changes, and enforce configuration standards in CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented ESLint config export step runs project JavaScript, which can expose local or CI secrets when used on untrusted code.

Mitigation: Generate JSON snapshots only from trusted projects, or run the export in a disposable sandbox or container with no secrets, no credential mounts, restricted network access, and a read-only repository mount.

Risk: The security verdict is suspicious because the skill lacks a warning about executing project JavaScript during export.

Mitigation: Review the skill carefully before installing and avoid running the export step on untrusted pull requests or privileged CI runners.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/eslint-flat-config-validator)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text, JSON, or summary output with validation findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish success, validation failures, and file or parse errors.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
