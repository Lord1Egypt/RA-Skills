## Description: <br>
Lets two OpenClaw agents negotiate, coordinate, and commit to tasks in real time with peer-to-peer task negotiation, commitment tracking, deadline reminders, relay-based connection setup, and end-to-end encrypted messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techtanush](https://clawhub.ai/user/techtanush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let two agents negotiate task splits, confirm commitments, track deadlines, and record agreed work in local memory. It is suited for peer collaboration workflows where humans approve proposals before commitments are logged. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local identity keys and collaboration state. <br>
Mitigation: Keep the workspace private, protect generated Diplomat Address tokens, and verify that the private key remains in the local skill directory. <br>
Risk: The skill reads and writes collaboration memory and can inject peer and commitment summaries into agent context. <br>
Mitigation: Review proposed memory changes, keep commitments concise, and confirm that only expected workspace memory is being surfaced. <br>
Risk: The skill uses a default external relay or a relay URL supplied by environment configuration. <br>
Mitigation: Review the relay URL before connecting, use a self-hosted relay for tighter control, and treat public IP and relay-token metadata as sensitive. <br>
Risk: Inbound proposals and check-in prompts may influence future agent behavior. <br>
Mitigation: Manually verify inbound proposals, counter-proposals, deadlines, and check-ins before accepting or recording commitments. <br>
Risk: A manually started listener or optional deadline reminder may run beyond a single interaction. <br>
Mitigation: Start listener and reminder processes only when needed, monitor their status, and stop them when peer collaboration is no longer active. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/techtanush/claw-connector) <br>
- [Publisher profile](https://clawhub.ai/user/techtanush) <br>
- [Source repository](https://github.com/techtanush/claw-diplomat) <br>
- [Support issues](https://github.com/techtanush/claw-diplomat/issues) <br>
- [Release changelog](https://github.com/techtanush/claw-diplomat/releases) <br>
- [README](artifact/README.md) <br>
- [Implementation guide](artifact/IMPLEMENTATION.md) <br>
- [Relay README](artifact/relay/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal command guidance with local JSON and memory file updates performed by the skill scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable negotiation prompts, status summaries, peer and commitment records, encrypted relay messages, and local memory entries.] <br>

## Skill Version(s): <br>
2.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
