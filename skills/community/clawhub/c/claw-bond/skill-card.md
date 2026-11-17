## Description:

Lets two OpenClaw agents negotiate, coordinate, and commit to tasks in real time for peer-to-peer task negotiation, commitment tracking, and deadline reminders, using a relay for setup with end-to-end encrypted messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techtanush](https://clawhub.ai/user/techtanush)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Claw Connector to connect OpenClaw agents, negotiate task splits with explicit human approval, record accepted commitments, and surface deadline check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Peer-provided data and address tokens can persistently influence the agent through saved commitments and resurfaced notifications.

Mitigation: Review peer proposals and address tokens before accepting them, connect only with trusted peers, and periodically inspect saved peer and commitment records.

Risk: Network access can extend beyond the default relay when users configure an alternate relay URL.

Mitigation: Verify that each address token uses the expected relay and set DIPLOMAT_RELAY_URL only to a relay the user controls or trusts.

Risk: Runtime dependencies and the listener process affect the local agent environment.

Mitigation: Install in an isolated environment, pin Python dependencies, and run the listener only when collaboration with trusted peers is needed.

## Reference(s):

- [ClawHub listing for Claw Connector](https://clawhub.ai/techtanush/skills/claw-bond)
- [README.md](artifact/README.md)
- [Implementation guide](artifact/IMPLEMENTATION.md)
- [Permissions declaration](artifact/permissions.json)
- [ClawHub marketplace metadata](artifact/clawhub.yaml)
- [Relay README](artifact/relay/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with command examples, plus local JSON and Markdown state files created by the skill]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-confirmed negotiation prompts, peer and commitment status, deadline reminders, and local commitment records.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
