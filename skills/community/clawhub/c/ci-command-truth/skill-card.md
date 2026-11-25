## Description:

Statically checks GitHub Actions run commands for references to scripts, build targets, files, and local Python modules that do not exist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check GitHub Actions workflows before pushing or when investigating CI failures caused by missing scripts, targets, files, or Python modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions use a Git URL that could retrieve changed code, and the partial scan leaves the security review incomplete.

Mitigation: Review the installer and tool source; prefer a vetted package or a Git revision pinned to an audited commit, and install and run it in isolation without unnecessary credentials or filesystem access.

## Reference(s):

- [CI Command Truth on ClawHub](https://clawhub.ai/raktikoo/skills/ci-command-truth)
- [CI Command Truth source repository](https://github.com/RakTikoo/ci-command-truth)

## Skill Output:

**Output Type(s):** [Text, JSON, SARIF, GitHub annotations]

**Output Format:** [Text, JSON, SARIF 2.1.0, or GitHub annotation lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports checked, skipped, and unscanned commands with findings; it does not execute repository commands.]

## Skill Version(s):

0.4.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
