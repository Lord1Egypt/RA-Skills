## Description:

ClawHub skill publishing conventions \u2014 file inclusion rules, metadata requirements, versioning, and scanner false-positive defense.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almohalhel1408](https://clawhub.ai/user/almohalhel1408)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill when preparing or updating ClawHub skills so they can align packaging, metadata, versioning, publishing, and scanner-response practices with observed ClawHub behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or Docker commands copied from the guidance could affect a real ClawHub release or use mutable local image tags.

Mitigation: Review commands before running them, set an explicit release version, and confirm image tags and publish targets in the local environment.

Risk: Packaging or scanner guidance can become stale as ClawHub behavior changes.

Mitigation: Verify current ClawHub publish and inspect results for the target skill before relying on the guidance for a release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/almohalhel1408/skills/clawhub-publish-conventions)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables and inline shell, YAML, Dockerfile, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; examples should be reviewed before use in a real publishing workflow.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
