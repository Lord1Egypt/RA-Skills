## Description:

Echoes user input with an optional `Echo:` or `You said:` prefix for testing skill routing and message handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theeightt](https://clawhub.ai/user/theeightt)

### License/Terms of Use:


## Use Case:

Developers and testers use this skill to verify echo behavior, skill routing, and message passing by asking an agent to repeat supplied text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Echo output may be unreliable because the artifact's output format asks the agent to append an unsolicited greeting despite the exact-echo purpose.

Mitigation: Review and correct the echo instructions before using the skill for routing tests or exact-output checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theeightt/skills/echo-repeater)
- [ClawHub publisher profile](https://clawhub.ai/user/theeightt)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [String]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response is expected to echo the requested text, optionally prefixed with `Echo:` or `You said:`.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
