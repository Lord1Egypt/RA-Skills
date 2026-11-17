## Description:

Configures China-friendly mirror sources for common developer tools, including npm, pip, Go, Docker, Cargo, Maven, Gradle, Homebrew, and Git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironmanc2014](https://clawhub.ai/user/ironmanc2014)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and switch package-manager, container, language-toolchain, and Git proxy settings to China-region mirrors when default sources are slow or time out.

### Deployment Geography for Use:

Global; designed for China-region developer network environments.

## Known Risks and Mitigations:

Risk: Persistent mirror changes can alter dependency sources across local developer tools and may overwrite existing Cargo or Docker configuration.

Mitigation: Run status checks first, configure only reviewed tools, and back up existing Cargo and Docker configuration before applying changes.

Risk: Trusted-host pip settings and broad Go checksum bypasses can reduce dependency integrity protections.

Mitigation: Avoid trusted-host and GONOSUMDB=* settings unless the tradeoff is understood; prefer controlled mirrors and keep checksum validation enabled where possible.

Risk: Public or community mirrors may be unsuitable for production or CI dependency supply chains.

Mitigation: Use organization-controlled mirrors for production and CI systems.

## Reference(s):

- [Domestic Mirror Source List](references/mirrors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend status checks, reset commands, and selective use of the bundled setup script.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
