## Description:

Helps users inspect and manage macOS default applications and file associations, including extensions, UTIs, MIME types, and URL schemes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsonglew](https://clawhub.ai/user/tsonglew)

### License/Terms of Use:

MIT-0

## Use Case:

Mac users can use this skill to identify current and compatible handlers, review proposed association changes, and restore prior defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Association changes may affect which applications open files or links; optional event delivery may include local paths and full change plans.

Mitigation: Review the exact changes before approval. For monitoring or HTTPS event delivery, use a trusted tool and a destination you control.

## Reference(s):

- [Dutis on ClawHub](https://clawhub.ai/tsonglew/skills/dutis)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell command examples and TOML plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Association changes require explicit approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
