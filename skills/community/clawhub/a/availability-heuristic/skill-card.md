## Description:

Guides agents to check probability and risk estimates against reference-class base rates when vivid or recent examples may skew judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, planners, and decision-makers use the skill to evaluate estimates shaped by memorable events and document a more base-rate-grounded correction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example statistics may be inaccurate or unsuitable for the case, leading to a misleading base-rate correction.

Mitigation: Check the original data source and confirm that it represents the relevant reference class before relying on example statistics.

Risk: Calibration logs may retain sensitive details about individual cases.

Mitigation: Review what case details are recorded and minimize or remove identifying information from calibration logs.

## Reference(s):

- [Sources and further reading](references/sources.md)
- [Availability Heuristic skill page](https://www.deciqai.com/c/availability-heuristic)
- [ClawHub release page](https://clawhub.ai/deciqai/skills/availability-heuristic)
- [Stanford HAI AI Index](https://hai.stanford.edu/ai-index)
- [International Labour Organization](https://www.ilo.org/)
- [Project repository (linked from the skill)](https://github.com/deciqAI/knowledge-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured text with a Markdown estimate template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a reference class, base rate and source, availability-distortion checks, corrected estimate, decision implications, and calibration notes.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
