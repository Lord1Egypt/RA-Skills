## Description:

Helps an agent detect when recent tool calls are becoming repetitive or stuck and returns ON_TRACK, REPEATING, or STUCK with evidence and a suggested next step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill during long or stalled tasks to check whether recent tool use is repeating and to choose one new next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required ClawPhylax plugin keeps a local ledger of request and tool-outcome history for repetition checks.

Mitigation: Enable the plugin only when local session activity recording is acceptable; otherwise proceed without it and state what could not be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/am-i-going-in-circles)
- [ClawPhylax homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands]

**Output Format:** [Markdown text with an ACTION line, evidence, a do-not instruction, and a next-step recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use the local ClawPhylax plugin to inspect recent request and tool-outcome history; without it, the agent should state what could not be verified.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
