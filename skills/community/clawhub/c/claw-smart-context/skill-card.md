## Description:

Token-efficient agent behavior - response sizing, context pruning, tool efficiency, and delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe3112](https://clawhub.ai/user/joe3112)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to make an assistant more concise and cost-aware during routine work. It guides response sizing, context loading, tool-call batching, and delegation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make an agent more terse and less likely to perform redundant checks on low-risk work.

Mitigation: Override the skill or require explicit verification when careful review, safety, security, or high-stakes accuracy matters.

Risk: The skill encourages avoiding tools when an answer appears possible from context, which can be unsuitable for current or source-grounded questions.

Mitigation: Require source checks for time-sensitive, niche, legal, financial, medical, security, or otherwise high-accuracy tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joe3112/skills/claw-smart-context)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands]

**Output Format:** [Plain text or Markdown guidance, with shell commands only when task-relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Promotes concise responses, targeted context loading, batched independent tool calls, and reduced redundant checks for low-risk work.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
