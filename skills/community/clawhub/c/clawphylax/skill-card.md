## Description:

ClawPhylax helps OpenClaw agents choose and run one of 22 ClawPhylax checks for verifying actions, sends, failures, risk, repetition, compaction loss, cost, and related session evidence from a local plugin ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to identify the appropriate ClawPhylax plugin question, installation path, command, and expected verdict when checking whether an action worked, a message went out, risk is acceptable, or a long-running session stayed coherent. It is a guide for using the separate local ClawPhylax plugin rather than a replacement for the more specific question-focused skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The related ClawPhylax plugin keeps a persistent local ledger of agent requests, tool outcomes, and session history.

Mitigation: Install and enable the plugin only when the user is comfortable with that local record, and disclose what could not be verified if the plugin is unavailable.

Risk: Several checks depend on history recorded by the local plugin, so answers can be incomplete when the ledger is absent or lacks relevant events.

Mitigation: Treat plugin verdicts as evidence-backed guidance, follow the first-line action, and ask the user or continue without verification when the skill's procedure says evidence is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/clawphylax)
- [Publisher profile](https://clawhub.ai/user/aeneassoft)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing guidance for selecting ClawPhylax checks and interpreting verdicts; it does not itself execute plugin checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
