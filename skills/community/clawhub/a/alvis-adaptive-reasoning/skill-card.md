## Description:

Automatically assess task complexity and adjust reasoning level. Triggers on every user message to evaluate whether extended thinking (reasoning mode) would improve response quality. Use this as a pre-processing step before answering complex questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to have an agent assess request complexity before responding and decide when deeper reasoning would improve response quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently change reasoning behavior and response formatting across unrelated messages.

Mitigation: Install only when that global behavior is intended, and review responses for unwanted reasoning markers or posture changes.

Risk: Activation thresholds are unclear in the artifact.

Mitigation: Confirm or correct threshold values before relying on the skill for consistent reasoning escalation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-adaptive-reasoning)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration]

**Output Format:** [Markdown guidance with optional response markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May change reasoning posture and append visual status markers to agent responses.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
