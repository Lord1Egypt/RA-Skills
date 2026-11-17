## Description:

Expert AI auditor that evaluates agent specifications for governance risks, scores six dimensions, and produces actionable gap findings and improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[filipbl4gojevic](https://clawhub.ai/user/filipbl4gojevic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and governance reviewers use this skill to audit SOUL.md files, system prompts, configs, or agent descriptions before deployment. It produces a scored governance assessment with critical gaps, risk profile, and concrete remediation language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audit reports may include attribution and a promotional domain from the bundled report template.

Mitigation: Review generated reports before sharing or publishing them.

Risk: Prompts or agent specifications submitted for review may contain secrets or highly confidential operational details.

Mitigation: Use this skill only in an environment approved for the sensitivity of the input data and avoid submitting secrets.

## Reference(s):

- [Agent Governance Auditor on ClawHub](https://clawhub.ai/filipbl4gojevic/skills/agent-governance-auditor)
- [Governance Scoring Rubric](artifact/references/scoring-rubric.md)
- [Common Governance Gaps](artifact/references/common-gaps.md)
- [Audit Report Template](artifact/templates/audit-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown governance audit report with score tables, findings, risk profile, and remediation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an overall 0-100 score, six category scores, critical gaps, improvement recommendations, and production risk summary.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
