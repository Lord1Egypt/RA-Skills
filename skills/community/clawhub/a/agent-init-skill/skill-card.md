## Description:

Initializes or updates project-level AGENTS.md or CLAUDE.md instructions by analyzing a project and restructuring the result into a nine-section agent onboarding template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or refresh repository-level guidance for AI coding agents. It helps produce AGENTS.md or CLAUDE.md files that document project structure, commands, conventions, local validation, and available documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or rewrite project-level agent instruction files, which can affect how agents behave in a repository.

Mitigation: Review generated or modified AGENTS.md and CLAUDE.md files before committing or relying on them.

Risk: The skill includes a self-evolution workflow that can persist failure notes and propose changes to the skill itself.

Mitigation: Allow the self-evolution workflow only when explicitly desired, and review any diary or SKILL.md changes separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orbisz/skills/agent-init-skill)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown file with tables, bullet lists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets AGENTS.md or CLAUDE.md in the project root and may include TODO markers for genuinely unavailable facts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
