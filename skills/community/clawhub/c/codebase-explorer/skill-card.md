## Description:

Analyze unfamiliar codebases and generate structured onboarding guides with architecture maps, entry points, conventions, and project-specific instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand unfamiliar repositories, map architecture and entry points, identify project conventions, and draft onboarding guidance or project-specific CLAUDE.md instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CLAUDE.md content can influence future agent behavior if it is incorrect or too broad.

Mitigation: Review any generated CLAUDE.md before keeping it and keep only project-specific, accurate instructions.

Risk: Repository scans may miss conventions or commands when project structure is unusual or ambiguous.

Mitigation: Verify generated onboarding notes against the actual code and configuration, and preserve explicit unknowns instead of guessing.

## Reference(s):

- [Reconnaissance Phase](references/reconnaissance.md)
- [Onboarding Artifacts](references/artifacts.md)
- [ClawHub Skill Page](https://clawhub.ai/djc00p/skills/codebase-explorer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance, Shell commands]

**Output Format:** [Markdown with structured sections, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce an onboarding guide and starter CLAUDE.md content for review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
