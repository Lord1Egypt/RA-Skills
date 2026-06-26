## Description: <br>
Enables secure peer-to-peer task negotiation and commitment tracking between two OpenClaw agents through an external relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techtanush](https://clawhub.ai/user/techtanush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to connect two agents, negotiate task commitments, record agreed terms, and surface deadlines for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Negotiations and handoffs pass through an external relay and may include sensitive task context. <br>
Mitigation: Use trusted peers, avoid placing secrets in proposals or handoffs, and self-host or override the relay when operational control is required. <br>
Risk: The skill starts a background listener and writes local commitment, peer, and key files under skills/claw-diplomat. <br>
Mitigation: Install only when inbound agent-to-agent negotiation is desired, monitor the listener process, and protect the skills/claw-diplomat directory, especially diplomat.key. <br>
Risk: Commitment records are appended to local memory files and surfaced back into agent context. <br>
Mitigation: Review negotiated terms before approval and keep proposals free of confidential material that should not be persisted or resurfaced. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/techtanush/claw-diplomat) <br>
- [Publisher profile](https://clawhub.ai/user/techtanush) <br>
- [ClawHub metadata homepage](https://clawhub.io/skills/claw-diplomat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-oriented text emitted through OpenClaw skill commands and hooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces address tokens, peer connection status, negotiated commitment summaries, check-in reminders, and local commitment records.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
