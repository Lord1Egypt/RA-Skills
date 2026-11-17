## Description:

Advisor Board helps agents produce decision consultation reports by combining web-search context with multiple named advisory frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mambamentatily24](https://clawhub.ai/user/mambamentatily24)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze business, product, investment, life-planning, strategy, and technical questions through a structured advisory-board workflow. The skill produces a consultation report with web-search findings, advisor perspectives, recommendations, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic web searching can expose sensitive prompts or regulated information to retrieval systems.

Mitigation: Avoid entering secrets or regulated data unless search behavior is acceptable and controls to disable or limit search are available.

Risk: The skill stores consultation, retrieval, feedback, and follow-up records without clear consent, retention, or deletion controls.

Mitigation: Review local memory behavior before use, avoid sensitive inputs, and confirm there are controls to skip saving records, delete history, and opt out of follow-ups.

Risk: Decision-advisory outputs may influence personal, business, investment, or technical decisions.

Mitigation: Treat reports as decision support, verify important claims independently, and apply human review before acting.

## Reference(s):

- [Advisor Board on ClawHub](https://clawhub.ai/mambamentatily24/skills/advisor-board)
- [Advisor Profiles](references/advisor-profiles.md)
- [Mindmap](references/mindmap.md)
- [Quality Assurance](references/quality-assurance.md)
- [Quick Reference](references/quick-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown consultation report with web-search findings, advisor viewpoints, recommendations, and action checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save consultation, retrieval, feedback, and follow-up records to local memory paths described by the artifact.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
