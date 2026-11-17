## Description:

Curiosity Engine adds structured self-questioning, assumption checking, information-gap detection, and tool-driven exploration behaviors to OpenClaw agents for open-ended or uncertain tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luofulily1-cmyk](https://clawhub.ai/user/luofulily1-cmyk)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to make an OpenClaw agent spend extra reasoning effort on open-ended research, anomaly investigation, deep analysis, and uncertainty reduction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broader tool-driven exploration, including shell execution, which can increase exposure to unsafe commands or unnecessary data access.

Mitigation: Keep shell execution and file reading controlled by normal user approval and sandbox policy.

Risk: Optional persistence of open threads can retain future-question context across sessions.

Mitigation: Opt into memory only when retaining that context is acceptable for the deployment.

Risk: Extra exploration can produce incorrect or misleading guidance if the agent over-extends beyond verified evidence.

Mitigation: Review generated analysis and scan the skill before deployment, especially when outputs affect operational decisions.

## Reference(s):

- [Curiosity Engine on ClawHub](https://clawhub.ai/luofulily1-cmyk/skills/curiosity-engine)
- [Curiosity Engine Examples](references/examples.md)
- [Theoretical Foundations](references/theory.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response guidance with optional shell command or tool-use suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full activation can include confidence ratings, surprise notes, and open threads; light activation adds extra depth without the full visible structure.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
