## Description:

Branerail guides Claude Code users through CTO-level architecture work, including design-first planning, state ownership, resilience, observability, dependency analysis, and architectural review of AI-generated code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uditakhourii](https://clawhub.ai/user/uditakhourii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to plan systems before implementation, audit AI-generated code for architectural soundness, and document resilience, observability, state ownership, and dependency decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intentionally broad and may influence many architecture, refactoring, resilience, observability, and code review conversations.

Mitigation: Install it only when broad architectural guidance is desired, and review recommendations against project-specific requirements before applying them.

Risk: Supporting documentation includes commands and publishing workflows that could copy files, run package tooling, or publish artifacts if followed directly.

Mitigation: Review commands before execution, pin or sandbox package tooling, and run publishing steps only when intentionally releasing the package publicly.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/uditakhourii/skills/branerail)
- [Architectural Specification Template](references/spec_template.md)
- [DESIGN.md Template](references/DESIGN_template.md)
- [Code Review Checklist](references/code_review_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, templates, code examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include architectural analysis, implementation review findings, specification drafts, DESIGN.md content, and concrete remediation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
