## Description:

v1.2 error recovery guidance for agent workflows, covering tiered retry strategies, consensus fallback, loop detection, degradation notices, and long-conversation recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide agents through tool-call failures, repeated-error loops, backend degradation, and context truncation without repeating the same failed approach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may install missing dependencies automatically without clear approval or package-source controls.

Mitigation: Require the agent to identify the package from a trusted manifest and ask before installing an exact version.

## Reference(s):

- [ClawBrain dashboard](https://clawbrain.dev/dashboard)
- [ClawHub skill page](https://clawhub.ai/michaelfeng/skills/clawbrain-pro-retry)
- [Publisher profile](https://clawhub.ai/user/michaelfeng)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-user-invocable skill guidance for agent retry and recovery behavior.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
