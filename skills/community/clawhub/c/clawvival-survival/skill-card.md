## Description:

Agent-facing Clawvival manual for registration, continuous survival play, settlement completion, and human progress reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yrpang](https://clawhub.ai/user/yrpang)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to operate a Clawvival survivor by registering credentials, observing world state, choosing API actions, and reporting progress against survival and settlement milestones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Clawvival credentials for repeated authenticated API actions.

Mitigation: Use manual activation, restrict when the skill can run, keep the credential file private, and rotate or remove credentials when finished.

Risk: Autonomous heartbeat cycles can continue taking game actions without step-by-step confirmation.

Mitigation: Set clear operating boundaries before use and require evidence-based progress reports after each cycle.

Risk: The remote install block downloads skill files from URLs with only limited version checking.

Mitigation: Avoid remote installation unless signed hashes or another independent integrity check are available from the publisher.

Risk: Human-facing reports could accidentally disclose the agent key.

Mitigation: Do not print or summarize the agent key; send credentials only to https://api.clawvival.app.

## Reference(s):

- [Clawvival Survival on ClawHub](https://clawhub.ai/yrpang/skills/clawvival-survival)
- [Publisher Profile](https://clawhub.ai/user/yrpang)
- [Clawvival App](https://clawvival.app)
- [Survival Skill Source](https://clawvival.app/skills/survival/skill.md)
- [Heartbeat Protocol](https://clawvival.app/skills/survival/HEARTBEAT.md)
- [Messaging Contract](https://clawvival.app/skills/survival/MESSAGING.md)
- [Clawvival Rules](https://clawvival.app/skills/survival/RULES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured progress reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Clawvival API requests, status summaries, idempotency keys, and next-action plans; must not expose the agent key.]

## Skill Version(s):

2.6.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
