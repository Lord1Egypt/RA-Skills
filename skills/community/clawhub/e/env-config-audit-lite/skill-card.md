## Description:

Compare .env against .env.example — missing keys, extra keys, and empty values on required-looking vars. Local files only, values never printed. Use when the user asks why an app fails on missing env vars or to check env config parity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to compare local environment files and identify missing, extra, or empty variable keys when troubleshooting configuration parity. It reports key names without exposing variable values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security verdict has medium confidence, and scanner coverage was partial.

Mitigation: Review the skill before installation and consider the stated local environment-file comparison purpose; use it only with files the user intends to compare.

Risk: Environment files may contain live credentials.

Mitigation: Keep comparisons local, share key names only, and do not echo or commit environment-file contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nenadzivotic/skills/env-config-audit-lite)

## Skill Output:

**Output Type(s):** [Analysis, JSON]

**Output Format:** [JSON report listing environment variable key names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Values are not included; comparison is structural and does not validate value formats or secret quality.]

## Skill Version(s):

1.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
