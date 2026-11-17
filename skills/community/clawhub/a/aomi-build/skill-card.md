## Description:

Aomi Build helps agents scaffold Aomi apps and plugins from API documentation, OpenAPI or Swagger specs, SDK references, or product requirements, producing Rust SDK crates with tool schemas, preambles, host interop flows, and validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceciliaz030](https://clawhub.ai/user/ceciliaz030)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn API specs, SDK references, or integration requirements into Aomi SDK app or plugin scaffolds. It is intended for builder workflows that need generated Rust code, a curated agent tool surface, host handoff patterns, and compile or test guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and build workflow can run mutable Rust code with broader access than the skill clearly scopes.

Mitigation: Review the skill before installing, pin the Aomi SDK to a release or commit, and inspect generated files before running Cargo builds.

Risk: Generated trading or wallet tools can become high-impact code if used against production accounts or networks.

Mitigation: Require explicit confirmation, use limits, prefer sandbox or testnet defaults, and review generated transaction or wallet handoff logic before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ceciliaz030/skills/aomi-build)
- [Aomi Build Homepage](https://github.com/aomi-labs/skills/tree/main/aomi-build)
- [Aomi SDK Repository](https://github.com/aomi-labs/aomi-sdk)
- [Aomi SDK Patterns](artifact/references/aomi-sdk-patterns.md)
- [Spec To Tools](artifact/references/spec-to-tools.md)
- [Host Routes](artifact/references/host-routes.md)
- [Build Examples](artifact/references/examples.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Security Posture](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Rust code, shell commands, configuration snippets, and generated source file plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Aomi app files such as lib.rs, client.rs, tool.rs, Cargo.toml, generated OpenAPI clients, and build artifacts when used by an agent with filesystem and cargo access.]

## Skill Version(s):

0.1.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
