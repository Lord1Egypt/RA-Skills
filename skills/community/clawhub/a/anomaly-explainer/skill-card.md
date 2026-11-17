## Description:

Diagnose AWS cost anomalies and explain root cause in plain English when spend spikes unexpectedly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Cloud and FinOps teams use this skill to triage AWS spend spikes by identifying the affected service, account, region, time window, likely root cause, and practical containment or prevention steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The user may need to share AWS cost, billing, and incident details for diagnosis.

Mitigation: Install and use the skill only when sharing those AWS cost and incident details is acceptable.

Risk: Generated containment or prevention actions may be incorrect or unsuitable for the user's AWS environment.

Mitigation: Review recommendations before applying changes in AWS.

## Reference(s):

- [Anomaly Explainer on ClawHub](https://clawhub.ai/anmolnagpal/skills/anomaly-explainer)
- [Publisher profile: anmolnagpal](https://clawhub.ai/user/anmolnagpal)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown incident response summary with a Slack-ready one-liner and Jira ticket body]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence level, probable root cause, supporting evidence, estimated impact, containment action, and prevention recommendation.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
