## Description:

Automatically assess task complexity and adjust reasoning level before answering complex questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to help an agent decide when a request warrants deeper reasoning before responding. It is intended as a mental pre-processing aid for complex, ambiguous, architectural, mathematical, or high-stakes requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic reasoning activation may surprise users who expect explicit control over reasoning mode.

Mitigation: Install only when automatic complexity assessment is desired, and edit or avoid the skill when precise manual control is required.

Risk: Deeper reasoning can increase latency or token usage.

Mitigation: Use the skill for requests where higher response quality justifies additional reasoning cost.

Risk: Corrupted threshold markers in the artifact may make activation boundaries unclear.

Mitigation: Review and correct threshold values before relying on the skill for consistent reasoning-mode decisions.

Risk: Visible reasoning icons may be unwanted in some response styles.

Mitigation: Edit or avoid the visual indicator instructions if responses should not include reasoning-mode icons.

## Reference(s):

- [Adaptive Reasoning ClawHub Skill Page](https://clawhub.ai/alvisdunlop/skills/alvis2-adaptive-reasoning)
- [alvisdunlop Publisher Profile](https://clawhub.ai/user/alvisdunlop)

## Skill Output:

**Output Type(s):** [guidance, text, configuration]

**Output Format:** [Markdown or plain text guidance with optional reasoning-mode indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cause the agent to use deeper reasoning and append visible reasoning indicators for higher-complexity responses.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
