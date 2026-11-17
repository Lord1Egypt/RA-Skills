## Description:

Automatically assess task complexity and adjust reasoning level before answering complex questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxz9909](https://clawhub.ai/user/cxz9909)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to have an agent score request complexity and adjust response depth before answering complex, ambiguous, architectural, mathematical, or high-stakes tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently change reasoning mode and append icons to ordinary responses.

Mitigation: Use it only where response-format changes are acceptable, or revise the skill to require explicit opt-in before changing behavior.

Risk: Automatic icons and behavior changes can break workflows that require exact JSON, signatures, protocol text, or strict formatting.

Mitigation: Disable or modify the skill for strict-format workflows so user formatting instructions take precedence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxz9909/skills/cxz9909-adaptive-reasoning)
- [ClawHub publisher profile](https://clawhub.ai/user/cxz9909)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append reasoning-status icons to agent responses when higher complexity is detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
