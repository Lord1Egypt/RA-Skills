## Description:

Provides knowledge and guardrails for configuring the mise, fnox, and Infisical secrets-management toolchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[basher83](https://clawhub.ai/user/basher83)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect existing mise, fnox, and Infisical setup, configure secret injection patterns, and avoid unsafe environment-variable handling in local development and CI/CD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer examples include curl-to-shell commands that may execute unverified remote scripts.

Mitigation: Prefer verified package-manager installs or pinned release artifacts before following installer guidance.

Risk: Exporting secrets to .env, .env.local, or secrets.json can create plaintext secret material.

Mitigation: Keep exported secret files tightly controlled, gitignored, and limited to workflows that explicitly require them.

Risk: The skill inspects local secret-tool configuration and may surface sensitive paths or environment details.

Mitigation: Review generated guidance and command output before sharing it outside the trusted project context.

## Reference(s):

- [mise Integration Reference](references/mise-integration.md)
- [fnox Configuration Reference](references/fnox-configuration.md)
- [Infisical Patterns Reference](references/infisical-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local validation commands and references to project configuration files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
