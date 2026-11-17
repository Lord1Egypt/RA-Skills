## Description:

Analyzes adult home blood-pressure logs to summarize averages, flag measurement issues and concerning readings, compare home and clinic patterns, and prepare a clinician-facing report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

People reviewing adult home blood-pressure logs can use the skill to prepare a summary of trends, measurement concerns, and clinic comparisons for discussion with a clinician. It does not diagnose conditions or guide medication changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal blood-pressure logs contain sensitive health information.

Mitigation: Provide only the intended local CSV and handle its contents and resulting report as sensitive health information.

Risk: A log interpretation may be mistaken for a diagnosis or medication plan.

Mitigation: Use results as informational support for adult home logs and review concerns or treatment decisions with a clinician.

Risk: High readings with symptoms can require urgent attention.

Mitigation: Follow the skill's emergency guidance rather than relying on the report when high readings occur with symptoms.

## Reference(s):

- [BP Log Sentinel release](https://clawhub.ai/voronindenis5/skills/bp-log-sentinel)
- [Measurement protocol](references/measurement-protocol.md)
- [Interpreting home blood pressure](references/interpretation.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Plain-text report with averages, flags, clinic comparison when supplied, and a clinician-ready summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on a user-supplied local CSV; optional clinic reading enables comparison.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
