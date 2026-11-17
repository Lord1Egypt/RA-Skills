## Description:

Guides developers through building and packaging third-party Feiniu NAS fnOS FPK apps, including native and Docker apps, manifests, permissions, lifecycle scripts, UI entries, Open API integration, and testing or publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalingo81](https://clawhub.ai/user/dalingo81)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to produce fnOS FPK packaging guidance, shell commands, manifests, permission/resource configuration, lifecycle script examples, and Open API integration patterns for Feiniu NAS applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell examples could lead an agent to generate vulnerable NAS lifecycle scripts.

Mitigation: Review generated lifecycle scripts before use, validate or parse configuration files instead of sourcing them as shell, and avoid copying unsafe shell examples as-is.

Risk: The skill may suggest installing fnpack system-wide from a downloaded binary.

Mitigation: Verify fnpack from an authenticated source before installation and confirm the selected binary matches the target OS and architecture.

Risk: Generated packages could run with excessive privileges.

Mitigation: Keep apps running as the package user unless root is strictly required and justified for the specific application.

## Reference(s):

- [Feiniu fnOS Developer Documentation](https://developer.fnnas.com)
- [Feiniu Open API Overview](https://developer.fnnas.com/api/overview/)
- [fnpack 1.2.3 Download Pattern](https://static2.fnnas.com/fnpack/fnpack-1.2.3-{os}-{arch})

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fnpack and appcenter-cli command examples plus fnOS manifest, resource, privilege, UI, wizard, and lifecycle-script snippets.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
