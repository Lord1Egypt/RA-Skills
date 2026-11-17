## Description:

A powerful OpenClaw skill for managing and automating GPU container instances on CFGPU cloud platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r600a-code](https://clawhub.ai/user/r600a-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI/ML teams, researchers, and content creators use this skill to discover CFGPU resources and manage GPU container instance lifecycle operations through guided shell commands and API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be exposed or persisted insecurely during setup and API use.

Mitigation: Review and harden the shell scripts before deployment, avoid running setup-env.sh as-is, avoid storing real tokens in shell startup files, and rotate any token entered into this skill.

Risk: Create, stop, release, and change-image operations can affect billable GPU resources.

Mitigation: Require explicit confirmation before executing resource-changing operations, and review target instance IDs, image IDs, duration, and pricing before approving commands.

Risk: Unsafe shell command handling can increase risk when untrusted values are passed into scripts.

Mitigation: Review script command construction before use and avoid passing untrusted input into helper script arguments or configuration.

## Reference(s):

- [CFGPU API Reference](references/api-reference.md)
- [CFGPU Platform](https://cfgpu.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that call CFGPU APIs and change billable cloud resources.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
