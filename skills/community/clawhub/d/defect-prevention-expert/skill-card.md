## Description:

Defect Prevention Expert helps software teams run lifecycle quality assurance across requirements, design, coding, testing, release, and operations through prevention, review, measurement, and improvement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengqch](https://clawhub.ai/user/zengqch)

### License/Terms of Use:

MIT-0

## Use Case:

Software developers, QA engineers, and delivery teams use this skill to identify quality risks, review requirements, designs, code, and test cases, define quality gates, and produce improvement plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write reports or persistently modify shared checklists, examples, templates, and workflow documentation during or after reviews.

Mitigation: Run the skill in read-only review mode by default and require explicit user approval before any write to project or skill knowledge files.

Risk: The skill declares execute capability even though its normal quality-review workflows primarily produce analysis, reports, and recommendations.

Mitigation: Disable execution permission unless a separate, specific workflow justifies it and the command scope has been reviewed.

Risk: The artifact is a Chinese-language quality-review skill, so reviewers who cannot read Chinese may miss constraints or risk guidance.

Mitigation: Have Chinese-language outputs reviewed by a fluent reviewer or translate them before acting on recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zengqch/skills/defect-prevention-expert)
- [Review Checklist](artifact/checklists/review-checklist.md)
- [Quality Gate Workflow](artifact/docs/quality-gate-workflow.md)
- [Example Scenarios](artifact/examples.md)
- [Stage Output Templates](artifact/templates/stage-output-templates.md)
- [Concept Clarification](artifact/templates/concept-clarification.md)
- [Test Case Template](artifact/templates/test-case-template.md)
- [Test Report V3](artifact/TEST_REPORT_V3.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports, checklists, review findings, testing suggestions, quality metrics, and improvement plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are selected by lifecycle stage and may include severity, priority, risk descriptions, recommendations, and follow-up items.]

## Skill Version(s):

4.2.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
