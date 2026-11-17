## Description:

Helps an agent decide whether recent token use reflects execution, information gathering, repetition, or deliberation, then returns a specific next action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill during long OpenClaw tasks to check whether assistant turns are making progress, gathering useful context, repeating calls, or over-deliberating. It supports course correction by returning EXECUTING, RETURN_TO_PLAN, or STOP_REPEATING with the next call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required clawphylax workflow reads the current OpenClaw conversation transcript and usage metadata.

Mitigation: Install only when transcript access for token-behavior analysis is acceptable in the target environment.

Risk: Output-token attribution may be unavailable when the provider does not report usage.

Mitigation: Use turn counts as the fallback signal and avoid treating token-share figures as complete when usage data is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/am-i-using-too-many-tokens)
- [Project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown text with an ACTION line, token-use shares, repeated-call details, and NEXT guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the current OpenClaw conversation transcript through clawphylax; output-token attribution depends on provider usage reporting.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
