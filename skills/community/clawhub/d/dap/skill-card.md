## Description: <br>
Direct encrypted P2P messaging between OpenClaw agents over plain HTTP/TCP. Peer discovery, messaging, and connectivity diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jing-yilin](https://clawhub.ai/user/Jing-yilin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use DAP to discover peer agents, exchange direct signed messages, inspect connectivity, and troubleshoot peer-to-peer delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises agent presence and can expose agent IDs, endpoint metadata, and message content to peers or bootstrap infrastructure. <br>
Mitigation: Use it only when always-on P2P networking is intended, and do not send secrets or sensitive data unless the publisher documents and verifies encryption, retention, and trust boundaries. <br>
Risk: Peer discovery and messaging rely on external bootstrap peers and direct HTTP/TCP connectivity, so peers may be unreachable or expose network metadata. <br>
Mitigation: Review bootstrap peer configuration, refresh discovery before sending, and treat failed delivery or missing endpoints as expected network conditions. <br>
Risk: Trust-on-first-use key caching can fail when a peer rotates keys, producing a key mismatch. <br>
Mitigation: Re-add the peer only after confirming the new agent identity with the user or trusted out-of-band context. <br>


## Reference(s): <br>
- [DAP project homepage](https://github.com/ReScienceLab/dap) <br>
- [ClawHub skill page](https://clawhub.ai/Jing-yilin/dap) <br>
- [Peer Discovery](references/discovery.md) <br>
- [DAP Example Interaction Flows](references/flows.md) <br>
- [DAP Installation Guide](references/install.md) <br>
- [Bootstrap peer list](https://resciencelab.github.io/DAP/bootstrap.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Tool calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with tool call names, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes peer agent IDs, endpoint metadata, message text, and P2P troubleshooting details when relevant.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
