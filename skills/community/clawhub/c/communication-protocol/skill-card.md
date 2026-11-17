## Description:

Defines how the OpenClaw agent should communicate with Tidy during a build session, ensuring clear, predictable, and build-focused interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dweikanas](https://clawhub.ai/user/dweikanas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep OpenClaw build-session communication predictable, concise, and aligned with Tidy's structured event flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may expose transport metadata or internal orchestration language in user-facing build messages.

Mitigation: Follow the skill's communication guardrails and review generated messages for concise, user-facing language before deployment.

## Reference(s):

- [Communication Protocol ClawHub Skill](https://clawhub.ai/dweikanas/skills/communication-protocol)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with JSON event examples and structured communication rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise user-facing message guidance and structured event contract recommendations for Tidy build sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
