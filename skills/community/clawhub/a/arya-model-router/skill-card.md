## Description:

Routes OpenClaw tasks across cheap, default, pro, and ultra model tiers with overrides, feedback, response policies, and optional briefing to reduce token cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staratheris](https://clawhub.ai/user/staratheris)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route OpenClaw requests to an appropriate model tier, keep routine work on lower-cost models, and trigger briefing or sub-agent use for heavier tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README shell example can become command execution if raw user text is interpolated into a shell command.

Mitigation: Invoke router.py through a structured argument array or a wrapper that avoids shell interpolation for user-controlled text.

Risk: Automatic escalation to pro or ultra model tiers and sub-agents can increase cost or send more context than intended.

Mitigation: Review rules.json thresholds before deployment and require operator approval or logging for pro, ultra, and use_subagent actions.

Risk: state.json persists mode, last decision, and feedback data locally.

Mitigation: Store state in a controlled per-user location, limit filesystem access, and reset or rotate the file when retention is not needed.

## Reference(s):

- [Arya Model Router README](artifact/README.md)
- [ClawHub release page](https://clawhub.ai/staratheris/skills/arya-model-router)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON decision objects and plain-text briefs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decisions include model tier, selected model, score, reasons, actions, response policy, and helper command hints.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
