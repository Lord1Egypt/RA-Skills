## Description:

Compresses an OpenClaw agent's internal reasoning and planning prose into a concise telegraphic style while preserving final-response personality and technical syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricgu8086](https://clawhub.ai/user/ricgu8086)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to make an agent format its internal planning and reasoning notes more concisely while keeping user-facing answers and technical artifacts readable and accurate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause internal reasoning or planning text to appear in agent responses.

Mitigation: Review and revise the reasoning-disclosure behavior before routine use, especially in sensitive workflows.

Risk: The skill broadly changes how the agent formats reasoning and output behavior.

Mitigation: Enable it only when that behavior is desired and test the resulting responses before relying on it in production.

Risk: Local SOUL.md-style personality content may influence the agent's final output.

Mitigation: Keep local personality files trusted and review them before enabling this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricgu8086/skills/caveman-soul-optimizer)
- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- [mCo0L/caveman-claw](https://github.com/mCo0L/caveman-claw)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and prompt instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only behavior; no code execution is described in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
