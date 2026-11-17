## Description:

Let any agent produce code indistinguishable from the existing codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airscripts](https://clawhub.ai/user/airscripts)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Agentskill to analyze repositories and produce AGENTS.md guidance that helps coding agents match the target codebase's structure, conventions, workflows, and review expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects repositories named by the user, which can expose local project structure and source conventions to the active agent workflow.

Mitigation: Use it only on repositories you are comfortable having the agent inspect, and review the generated AGENTS.md before sharing it.

Risk: User-supplied remote references can influence the generated guidance.

Mitigation: Use remote references only from trusted sources and review any imported conventions before adopting the output.

Risk: Generated AGENTS.md guidance can be incorrect or too broad for the repository if evidence is incomplete.

Mitigation: Review the draft against the repository before relying on it for coding-agent behavior.

## Reference(s):

- [Agentskill ClawHub listing](https://clawhub.ai/airscripts/skills/agentskill)
- [Agentskill package on PyPI](https://pypi.org/project/agsk)
- [Turning Repository Knowledge Into Usable Agent Context](https://dev.to/airscript/turning-repository-knowledge-into-usable-agent-context-4pe4)
- [API Reference](docs/reference/README.md)
- [CLI Reference](docs/reference/cli.md)
- [Generation Gotchas](references/GOTCHAS.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown AGENTS.md documentation, with optional split or multifile markdown layouts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Skill mode authors AGENTS.md from analyzer evidence; CLI mode can emit deterministic markdown directly.]

## Skill Version(s):

1.4.0 (source: server release evidence, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
