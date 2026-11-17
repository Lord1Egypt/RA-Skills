## Description:

Navigate and understand codebases using agentlens hierarchical documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nguyenphutrong](https://clawhub.ai/user/nguyenphutrong)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to navigate large codebases through AgentLens documentation before reading source files, locating modules, symbols, warnings, dependencies, and generated file summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers agents to read and trust project-local .agentlens documentation before source files.

Mitigation: Treat .agentlens files as repository content: review their guidance before acting on warnings, TODOs, or regeneration instructions.

Risk: Generated AgentLens documentation may be stale relative to the source code.

Mitigation: Check source files before making changes when documentation appears outdated, and regenerate AgentLens docs when appropriate.

## Reference(s):

- [Navigation Patterns](references/navigation.md)
- [AgentLens Output Structure](references/structure.md)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown instructions and navigation patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs the agent to consult local .agentlens documentation before reading source files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; skill metadata lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
