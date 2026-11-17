## Description:

Use when configuring Maven plugins, setting up common plugins like compiler, surefire, jar, or creating custom plugin executions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build engineers use this skill to configure Maven build, test, quality, packaging, version-management, and code-generation plugins for Java projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maven plugin examples that run external commands can execute trusted or untrusted repository scripts during a build.

Mitigation: Use exec plugin configuration only with trusted scripts in trusted repositories, and review command paths and arguments before copying examples.

Risk: Release and version-management plugin examples can change project release state or dependency versions.

Mitigation: Review release, version, and update commands in a branch or CI dry run before applying them to protected repositories.

Risk: Manifest examples can embed developer identity or build timestamps, which may affect privacy or reproducible builds.

Mitigation: Remove Built-By and Build-Time manifest entries when privacy or reproducibility requirements apply.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/fix-build-google-auto-maven-plugin-configuration)
- [Java SE 17 API documentation](https://docs.oracle.com/en/java/javase/17/docs/api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with XML configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples should be reviewed before use in a project build.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
