## Description:

Cognitive Debt Guard helps agents and developers review AI-generated code with comprehension gates, review frameworks, and AI-free zones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill during AI-assisted code review to keep code understandable before it is accepted, merged, or maintained. It provides checklists for comprehension, data-flow tracing, AI-free zones, smaller PR scope, and quarterly comprehension audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake this lightweight review aid for an automated security control.

Mitigation: Use it alongside normal human review, security review, and scanning rather than as a standalone control.

Risk: Broad trigger language may cause the skill to appear during general code review prompts or suggest MEMORY.md updates that are not project-accurate.

Mitigation: Confirm the skill is relevant to the review and inspect any MEMORY.md updates before accepting them.

## Reference(s):

- [Cognitive Debt Guard on ClawHub](https://clawhub.ai/aptratcn/skills/cognitive-debt-guard)
- [Debt Indicators](DEBT_INDICATORS.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, review questions, templates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only review aid; no automatic code execution]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
