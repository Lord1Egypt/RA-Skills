## Description:

Architecture review based on OpenSpec documents and code, with multi-dimension evaluation, structured scoring, and actionable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdingiit](https://clawhub.ai/user/fdingiit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate software architecture against OpenSpec requirements and project structure. It produces a structured architecture report with dimension scores, strengths, weaknesses, prioritized recommendations, and issue triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project structure, OpenSpec documents, previous review reports, and relevant local files for architecture analysis.

Mitigation: Install and run it only in projects where local architecture details may be reviewed by the agent.

Risk: Generated reports may contain internal architecture details and file paths.

Mitigation: Review the report before sharing it outside the project or organization.

Risk: Architecture recommendations can be incomplete when specifications or project structure are missing or stale.

Mitigation: Validate recommendations with project owners before using them as implementation direction.

## Reference(s):

- [Architecture Review Dimensions](dimensions.md)
- [Report Template](report-template.md)
- [Example Architecture Review Report](examples.md)
- [ClawHub Skill Page](https://clawhub.ai/fdingiit/skills/architect-review)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown architecture review report with scoreboard, per-dimension findings, recommendations, selected and deferred issues, and hidden machine-readable metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local .arch-review/<date>-report.md file only after user confirmation; otherwise presents analysis in chat.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
