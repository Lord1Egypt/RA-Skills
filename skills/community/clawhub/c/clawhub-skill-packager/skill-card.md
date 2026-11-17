## Description:

Turn rough, partial, or broken ClawHub/OpenClaw skill material into one publish-ready skill bundle plus one separate plain-text review file using an inference-first, low-friction workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neomagnetar](https://clawhub.ai/user/neomagnetar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to convert draft, incomplete, or inconsistent ClawHub/OpenClaw skill material into a release-style skill package with a separate review record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to rewrite, normalize, and package skill files using inferred defaults.

Mitigation: Review the generated review file and final bundle before publishing or installing the resulting skill.

Risk: Input skills may include credentials, APIs, scripts, binaries, or elevated permission assumptions that affect deployment risk.

Mitigation: Confirm the packaged skill's runtime and security declarations before release, especially when the input skill uses external services or executable components.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/neomagnetar/skills/clawhub-skill-packager)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Configuration, Guidance]

**Output Format:** [A publish-ready skill bundle plus a separate plain-text review file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The review output records inferred fields, automatic fixes, publish-readiness notes, and handoff details.]

## Skill Version(s):

1.5.2 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
