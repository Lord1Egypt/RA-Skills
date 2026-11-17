## Description:

Lets two OpenClaw agents negotiate, coordinate, and commit to tasks in real time through peer-to-peer task negotiation, commitment tracking, and deadline reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techtanush](https://clawhub.ai/user/techtanush)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Claw Connector to connect two OpenClaw agents, negotiate task splits with explicit human approval, and track agreed commitments and deadlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Peer-controlled text can enter negotiation context and influence agent behavior.

Mitigation: Use the skill only with trusted peers, keep explicit human approval for proposals and commitments, and avoid including secrets in handoffs or proposals.

Risk: Generated address tokens and public IP hints are shared through the relay and with peers who receive a token.

Mitigation: Share tokens only with intended peers, rotate or revoke tokens when needed, and self-host the relay when stronger metadata control is required.

Risk: The release has review-worthy concerns around confusing proposal actions and relay-token controls.

Mitigation: Review before installing and do not rely on the skill for sensitive workflows until the prompt-injection and proposal-action mismatch concerns are fixed.

Risk: The skill requires Python dependencies and executable local scripts.

Mitigation: Install dependencies in a virtual environment with pinned versions and review the scripts before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/techtanush/skills/claw-connector)
- [ClawHub Publisher Profile](https://clawhub.ai/user/techtanush)
- [Claw Connector README](artifact/README.md)
- [Claw Connector Implementation Guide](artifact/IMPLEMENTATION.md)
- [Claw Connector Relay README](artifact/relay/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands and JSON-backed local state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local key, peer, ledger, token, memory, and relay configuration files in the OpenClaw workspace.]

## Skill Version(s):

2.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
