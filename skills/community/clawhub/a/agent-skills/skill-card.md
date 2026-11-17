## Description:

Agent Skills standard reference guide covering SKILL.md specification format, progressive loading, skill discovery and activation, authoring best practices, quality evaluation, description optimization, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-skill authors use this skill to create, validate, optimize, and evaluate Agent Skills using the standard SKILL.md format and supporting reference files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Script examples may lead an agent to run package-manager commands or file-changing commands in a user's environment.

Mitigation: Use pinned versions, review dependencies, run dry runs when available, and require explicit approval before commands download packages or modify files.

Risk: Poorly scoped or untested skill descriptions can cause false activation or missed activation in downstream agents.

Mitigation: Evaluate trigger behavior with representative positive and near-miss prompts before release.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [Agent Skills Specification Reference](references/spec.md)
- [Skill Authoring Guide](references/authoring.md)
- [Skill Authoring Anti-Patterns](references/anti-patterns.md)
- [Binding Scripts in Skills](references/using-scripts.md)
- [Products Supporting Agent Skills](references/products.md)
- [Agent Skills Official Documentation](https://agentskills.io)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
