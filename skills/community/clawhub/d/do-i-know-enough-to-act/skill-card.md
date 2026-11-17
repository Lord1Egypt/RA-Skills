## Description:

Helps an agent decide whether to act now, gather more context, or continue when balancing irreversible actions against excessive exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill before state-changing actions, after repeated failed writes or commands, or when an agent appears to be gathering context without making progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required ClawPhylax plugin maintains a local observe-only ledger of requests and tool outcomes.

Mitigation: Install only when that local logging model is acceptable; the reviewed skill itself is reported as not sending data out or performing destructive actions.

Risk: The act-versus-gather recommendation depends on a fixed classification of tool calls and may not count unrecognized plugin tools.

Mitigation: Treat the recommendation as decision support and review the evidence counts and proposed next call before irreversible actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/do-i-know-enough-to-act)
- [Publisher profile](https://clawhub.ai/user/aeneassoft)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown text with an ACTION line, evidence summary, and one next-step command or call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The first line is one of ACTION: ACT_NOW, ACTION: GATHER_FIRST, or ACTION: BALANCED.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
