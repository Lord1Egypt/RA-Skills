## Description:

Generates a .ai-context knowledge base for coding agents when setting up or refreshing project knowledge, creating tiered documentation optimized for agent comprehension and token efficiency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create or regenerate concise project knowledge for coding agents. It helps agents understand project purpose, architecture, design decisions, and active issues without repeatedly scanning the full repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated project context can become persistent agent-readable guidance that carries stale or untrusted repository text into future sessions.

Mitigation: Review generated Markdown before relying on it, especially for untrusted or externally contributed repositories.

Risk: Running the helper script can create or overwrite files under an existing .ai-context directory.

Mitigation: Back up or diff any existing .ai-context directory before generation or regeneration.

Risk: Generated knowledge is a starting point and may contain placeholders or incomplete architecture and decision details.

Mitigation: Fill in placeholders, verify claims against the actual codebase, and update the files when project structure or constraints change.

## Reference(s):

- [Writing Guide for AI Context Knowledge Base](references/WRITING-GUIDE.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Architecture Decision Records](https://adr.github.io/)
- [Project README Template](https://github.com/LinusBorg/project-readme-template)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown files and optional TypeScript/Bun shell workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a persistent .ai-context directory with SKILL.md, DYNAMICS.md, reference Markdown files, and maintenance guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
