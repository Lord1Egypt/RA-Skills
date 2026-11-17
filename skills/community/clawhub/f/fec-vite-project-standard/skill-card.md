## Description:

Guides developers in configuring and reviewing Vite applications and libraries, including plugins, environment variables, development servers, and build performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Frontend developers use this skill to create, review, and troubleshoot Vite project configuration while checking client-side secrets, development behavior, type checking, and production builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing private environment variables in a client bundle.

Mitigation: Review exposed prefixes and keep credentials on the server or build system before applying configuration changes.

Risk: Misconfigured development proxies or build splitting can change application behavior or performance.

Mitigation: Review proposed proxy and chunk settings for the project and verify the resulting development and production builds.

## Reference(s):

- [Vite Project Standard on ClawHub](https://clawhub.ai/bovinphang/skills/fec-vite-project-standard)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with Vite configuration examples and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes project-type assessment, environment-variable guidance, and build and development checks.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json, metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
