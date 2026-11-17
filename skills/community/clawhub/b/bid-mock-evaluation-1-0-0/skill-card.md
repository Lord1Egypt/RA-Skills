## Description:

A Chinese-language bid self-review skill that helps bidders analyze evaluation tables, simulate scoring, audit response coverage, and identify compliance issues for lawful self-checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External bidders and bid-response teams use this skill to review Chinese procurement or tender materials before submission. It turns evaluation tables and draft responses into scoring self-checks, coverage gap reports, evaluator-friendly evidence indexes, and compliance issue lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real bid documents can contain confidential, personal, or competitively sensitive information.

Mitigation: Use the skill only with materials you are authorized to process, and redact sensitive information where possible before analysis.

Risk: Legal and scoring analysis may be incomplete, outdated, or different from an actual evaluator's decision.

Mitigation: Treat outputs as self-check guidance and verify current law, scoring assumptions, and final bid decisions with qualified professionals.

Risk: Coverage or scoring conclusions can be wrong if source materials are incomplete or only keyword matches are available.

Mitigation: Provide complete evaluation tables, rejection clauses, bid response sections, and real evidence locations; manually confirm any extracted or matched criteria before relying on a report.

Risk: The skill could be misused to support fabricated evidence or unfair bid manipulation.

Mitigation: Restrict use to truthful self-review, real evidence supplementation, lawful clarification, and compliance checking; do not use it to invent evidence or evade requirements.

## Reference(s):

- [Mock Evaluation Method](artifact/references/mock-evaluation-method.md)
- [Score Point Navigation and Coverage Audit](artifact/references/score-point-navigation.md)
- [Compliance Review Method](artifact/references/compliance-review.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports with tables, optional JSON criteria and coverage hints, and optional shell commands for local parsing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are self-check guidance; legal, scoring, and bid decisions require human verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
