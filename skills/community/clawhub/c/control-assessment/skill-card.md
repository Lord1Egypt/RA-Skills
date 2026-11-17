## Description:

Evaluate individual framework controls against organizational documentation with evidence extraction, severity classification, and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

Apache-2.0

## Use Case:

Compliance, security, and audit teams use this skill to assess whether organizational documentation satisfies individual framework controls and to identify evidence, gaps, severity, and remediation recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads compliance documents supplied by the user and may include direct evidence quotes in its output.

Mitigation: Use it only with documents the agent is allowed to read and quote in assessment results.

Risk: The WebFetch allowance can retrieve URL-supplied documents or reference material.

Mitigation: Avoid providing sensitive URLs unless external retrieval and assessment of that content is intended.

## Reference(s):

- [Control Assessment on ClawHub](https://clawhub.ai/dangsllc/skills/control-assessment)
- [Publisher profile: dangsllc](https://clawhub.ai/user/dangsllc)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON assessment with extracted evidence, gap analysis, severity, recommendations, confidence, and reasoning.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct quotes from user-provided compliance documents.]

## Skill Version(s):

0.1.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
