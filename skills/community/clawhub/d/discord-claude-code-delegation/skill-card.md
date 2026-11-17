## Description:

Delegate work from an OpenClaw Discord controller bot to a Claude Code worker bot through a private Discord worker lane, then relay the final result back to the original DM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jini92](https://clawhub.ai/user/jini92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up, test, debug, and harden a private Discord controller-to-worker lane that delegates tasks to a Claude Code worker bot and relays the final result back to the original DM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public or broadly triggered worker lane could expose delegated tasks or cause unintended worker execution.

Mitigation: Use a private worker lane and restrict intake to one trusted controller bot, one lane, and a fixed task prefix such as [WORKER_TASK].

Risk: Lane-only success can be mistaken for a complete delegation flow.

Mitigation: Verify the full closed loop from controller DM to worker lane, worker reply, and relay back to the original controller DM.

Risk: Worker-side bot-message guards or channel-property mismatches can silently block trusted lane messages.

Mitigation: Keep default bot-message protections in place and add only a narrow allowlist exception that matches the runtime's actual channel field.

## Reference(s):

- [Discord Claude Code Delegation skill page](https://clawhub.ai/jini92/skills/discord-claude-code-delegation)
- [Current contract](references/current-contract.md)
- [Operations](references/operations.md)
- [Debug map](references/debug-map.md)
- [Architecture](references/architecture.md)
- [Example envelopes](examples/envelopes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [Markdown guidance with text task-envelope examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on a private Discord worker-lane setup, structured task envelopes, relay-back checks, and debugging steps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
