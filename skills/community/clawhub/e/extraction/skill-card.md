## Description:

Extracts design systems, architecture patterns, workflows, and methodology from codebases into reusable skills and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to analyze an existing codebase, identify reusable design, architecture, workflow, and methodology patterns, and turn those findings into reusable skills or Markdown documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan a whole repository and may surface private code, design decisions, or business-specific patterns in generated documentation.

Mitigation: Run it only on repositories approved for analysis and review generated files before committing, publishing, or copying them to another repository.

Risk: Generated skills and documentation can misstate architecture, design tokens, or reusable patterns if extraction findings are incomplete.

Mitigation: Ask the agent for a proposed file plan first, then review extracted outputs against the source files before accepting them.

Risk: Installation examples use mutable npx-based commands, which can change behavior over time.

Mitigation: Install only from a pinned, reviewed version or commit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/extraction)
- [Methodology Values](references/methodology-values.md)
- [Extraction Categories](references/extraction-categories.md)
- [Skill Quality Criteria](references/skill-quality-criteria.md)
- [Extraction Validation Checklist](references/validation-checklist.md)
- [Project Summary Template](references/output-templates/project-summary.md)
- [Design System Template](references/output-templates/design-system.md)
- [Skill Template](references/output-templates/skill-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation, skill files, and guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or copy generated files into docs/extracted/ and ai/skills/ locations in the target repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
