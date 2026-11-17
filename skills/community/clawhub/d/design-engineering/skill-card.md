## Description:

Orchestrates iterative design and frontend engineering work through research, planning, sub-agent execution, and validation loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design engineers use this skill to plan, coordinate, implement, and validate iterative frontend design work, especially when rendering choices, sub-agent coordination, or visual QA need explicit engineering discipline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinated sub-agent work may propose or apply frontend changes that affect important project files.

Mitigation: Review the plan and resulting diffs before execution on important projects, then run the build and validation checklist.

Risk: Project-local research or validation files may be created during iterative design work.

Mitigation: Keep generated files inside the project root and inspect them before sharing, committing, or releasing the project.

Risk: Visual or rendering guidance can be wrong for a specific browser, viewport, or performance constraint.

Mitigation: Validate with build checks, JavaScript syntax checks, CSS-to-JS integration checks, responsive spot checks, and reduced-motion checks.

## Reference(s):

- [Rendering Technology Decisions](references/rendering-decisions.md)
- [Sub-Agent Patterns for Design Work](references/subagent-patterns.md)
- [Validation Checklist - Post Sub-Agent Execution](references/validation-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate project-local research and validation files during frontend work.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
