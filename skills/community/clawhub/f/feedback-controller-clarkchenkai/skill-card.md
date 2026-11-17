## Description:

Feedback Controller is a closed-loop agent skill for correcting execution drift by comparing target and current states, localizing deviations, and choosing a correction or escalation path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarkchenkai](https://clawhub.ai/user/clarkchenkai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to diagnose workflow drift after a partial or unsatisfactory result and decide whether to retry, switch tools, narrow scope, rewrite locally, or escalate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic invocation can steer an agent into a diagnostic correction format when a normal answer may be expected.

Mitigation: Use the skill for correction or quality-control situations where a structured drift diagnosis is appropriate.

Risk: The skill can influence retry or escalation decisions in workflows with material consequences.

Mitigation: Apply its escalation guidance and require human review when approval, policy, missing context, or high-risk judgment blocks a safe correction.

## Reference(s):

- [Correction Patterns](references/correction-patterns.md)
- [Escalation Rules](references/escalation.md)
- [Wiener Reference](references/wiener.md)
- [ClawHub Skill Page](https://clawhub.ai/clarkchenkai/skills/feedback-controller-clarkchenkai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with a fixed six-section diagnostic structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ends with Target State, Current State, Observed Deviation, Error Source, Correction Strategy, and Escalation Decision sections.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
