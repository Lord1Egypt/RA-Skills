## Description:

Validate devcontainer.json files for VS Code Dev Containers, GitHub Codespaces, and DevPod.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check devcontainer.json files for syntax, structure, features, ports, lifecycle scripts, customizations, and security best-practice issues before using them locally or in CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation output is lint guidance and may not fully represent an organization's container security policy.

Mitigation: Review warnings before changing container security settings or relying on a passing result.

Risk: Security-related findings can affect privileged mode, container capabilities, lifecycle scripts, and default user behavior.

Mitigation: Use focused security validation when reviewing sensitive devcontainer settings and confirm remediation choices before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/devcontainer-validator)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Text, JSON, or one-line summary output with severity-tagged validation findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish clean validation, validation errors, and file or parse errors; strict mode exits nonzero on any issue.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
