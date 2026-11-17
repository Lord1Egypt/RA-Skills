## Description:

A self-improving feedback loop skill that works standalone or with intent-engineering and dark-factory to observe systems or executions, analyze performance, generate improvement suggestions, create regression tests, track goal alignment, and produce signed improvement reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze logs, plain-text observations, or structured outcome reports, then generate prioritized improvement suggestions, regression test data, alignment checks, and repeatable JSON reports for the next improvement cycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom suggestion rules can execute Python expressions when the analyzer evaluates rule conditions.

Mitigation: Use only trusted suggestion_rules files, review rules before installation, and remove or replace Python-evaluable conditions before use in automated or privileged environments.

Risk: The skill writes analysis, report, and update JSON files to the selected output directory.

Mitigation: Run it in a controlled workspace and review generated files before feeding them into another automation cycle.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielfoojunwei/skills/auto-feedback)
- [Feedback Loop v2 Operations Guide](references/operations_guide.md)
- [Alignment Values](references/alignment_values.json)
- [Scoring Weights](references/scoring_weights.json)
- [Suggestion Rules](references/suggestion_rules.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [JSON files with optional Markdown report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces observation.json, analysis.json, improvement_report.json, updated_observation.json, and optionally updated_specification.json.]

## Skill Version(s):

1.0.1 (source: server release metadata; skill frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
