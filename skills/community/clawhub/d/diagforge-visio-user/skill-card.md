## Description:

Bootstrap skill for DiagForge that helps an agent onboard into the DiagForge GitHub repository, understand the project structure, run the canonical cold-start smoke test, and begin using the Visio-based drawing loop safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qweadzchn](https://clawhub.ai/user/qweadzchn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to bootstrap into the DiagForge repository, follow the intended read order, validate the Visio bridge with the cold-start smoke test, and start figure reproduction work that can produce editable Visio assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to download and run external Python code while using VISIO_BRIDGE_TOKEN.

Mitigation: Use a reviewed commit, inspect the smoke-test scripts before execution, run in a constrained environment, and keep VISIO_BRIDGE_TOKEN secret and narrowly scoped.

Risk: The publishing package contains guidance only and depends on the external DiagForge repository for runtime behavior.

Mitigation: Validate the checked-out repository and run the canonical cold-start smoke test before beginning open-ended drawing work.

## Reference(s):

- [DiagForge GitHub repository](https://github.com/qweadzchn/DiagForge)
- [DiagForge Bootstrap on ClawHub](https://clawhub.ai/qweadzchn/skills/diagforge-visio-user)
- [qweadzchn publisher profile](https://clawhub.ai/user/qweadzchn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides repository cloning, document read order, smoke-test execution, and environment setup requiring git, python, and VISIO_BRIDGE_TOKEN.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence, created 2026-03-20; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
