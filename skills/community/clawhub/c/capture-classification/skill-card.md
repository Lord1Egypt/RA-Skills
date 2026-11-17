## Description:

Standard Operating Procedure (SOP) that routes unstructured text to Tasks or LanceDB based on urgency using atomic nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to classify captured notes or transcripts as actionable or informational, then route them to Google Tasks or vector memory with verification stops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured notes or transcripts may contain secrets, regulated data, or private material before routing.

Mitigation: Use the skill only when Google Tasks and vector memory are approved destinations for the captured data.

Risk: Misclassification can route actionable text to memory or informational text to tasks.

Mitigation: Follow the documented verification stop that requires exactly one valid classification before routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/capture-classification)
- [Publisher profile](https://clawhub.ai/user/zvirb)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [JSON log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Confirms the routed destination and action taken by the selected atomic node.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
