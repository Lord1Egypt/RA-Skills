## Description: <br>
Lets two OpenClaw agents negotiate, coordinate, and commit to tasks in real time with peer-to-peer task negotiation, commitment tracking, deadline reminders, and end-to-end encrypted relay setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techtanush](https://clawhub.ai/user/techtanush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Claw Connector to connect two agents, negotiate task splits, record commitments, and surface deadline or status check-ins with explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay-based collaboration can expose public IP metadata to the relay and sometimes to peers. <br>
Mitigation: Use a relay you trust or self-host the relay, and share address tokens only with intended peers. <br>
Risk: The skill persists local coordination data, including key, peer, ledger, token, and memory-related files. <br>
Mitigation: Review the local files and permissions after setup, and avoid placing secrets in proposals, handoffs, or commitment text. <br>
Risk: Commitment summaries may be added to agent context, which can affect later sessions. <br>
Mitigation: Review generated commitment summaries and keep listener or cron-style reminder setup as an explicit manual action. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/techtanush/claw-bond) <br>
- [README](README.md) <br>
- [Implementation guide](IMPLEMENTATION.md) <br>
- [Relay README](relay/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown and plain text guidance with shell commands and local JSON or Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local key, peer, ledger, token, and commitment records; network relay use depends on configured relay settings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
