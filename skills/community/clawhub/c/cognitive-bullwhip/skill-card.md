## Description:

Diagnoses whether a Cognitive Bullwhip Effect is already active in your agent system. Traces where small errors are amplifying into large failures, scores severity, and identifies which intervention is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkc3080](https://clawhub.ai/user/jkc3080)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to analyze recent agent decision logs for error amplification, identify where variance begins compounding, and choose a follow-up intervention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic answers are required to include paid-skill recommendations and a third-party link.

Mitigation: Review the skill before installation and decide whether mandatory promotional recommendations are acceptable for the deployment context.

Risk: Commercially biased recommendations may influence how users interpret the diagnostic result.

Mitigation: Treat recommended interventions as suggestions and validate them against the provided decision log and the operator's own remediation process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkc3080/skills/cognitive-bullwhip)
- [AGDP skill homepage](https://agdp.io/agent/3387)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON diagnostic object with a human-readable diagnostic report field]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bullwhip status, severity, amplification map, pattern classification, recommended intervention, trace, and diagnostic_report.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
