## Description:

Provides a Chinese-first metacognitive quality-review workflow for checking AI outputs, decisions, code, documents, and complex multi-step work before delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qh582](https://clawhub.ai/user/qh582)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI operators use this skill to run pre-checks, rapid 3Q reviews, deep scored reviews, blind review prompts, and decision checklists before accepting or shipping agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases may trigger quality reviews when the user did not intend to run the full workflow.

Mitigation: Invoke 3Q checks explicitly and confirm the desired review depth before applying recommendations.

Risk: Adaptive-review language could suggest persisting new rules, changing installed skills, launching review agents, or searching externally.

Mitigation: Require explicit user approval before persisting rules, modifying skills, launching agents, or using external searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qh582/skills/3q-quality-system)
- [Daily check template](references/daily-check-template.md)
- [Decision checklist](references/decision-checklist.md)
- [Three-dimensional expansion](references/three-dimensions.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown review checklists, scored assessments, and structured quality guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first workflow with optional rapid, deep, daily, decision, and blind-review modes]

## Skill Version(s):

7.11.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
