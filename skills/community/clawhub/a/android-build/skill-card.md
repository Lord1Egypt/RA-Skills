## Description:

A tool for downloading and configuring Android SDKs for projects, supporting Windows and macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-smith-max](https://clawhub.ai/user/noah-smith-max)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to detect Android and Flutter project dependencies, download missing SDK tooling, configure project or global environment variables, and run project builds on Windows or macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically download and run an unverified external executable.

Mitigation: Install only after confirming trust in the publisher and binary source, or prefer a release with vendored auditable source and pinned checksum or signature verification.

Risk: The wrapper can change environment variables or run builds on the local machine.

Mitigation: Review proposed changes and build commands before use, and run in a controlled project environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-smith-max/skills/android-build)
- [Publisher profile](https://clawhub.ai/user/noah-smith-max)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute platform-specific setup and build commands through the bundled wrapper.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
