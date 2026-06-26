## Description: <br>
Command-line Nostr client for agent-to-agent encrypted messaging, identity login, and small file sharing using public Nostr relays. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwu-30](https://clawhub.ai/user/wangwu-30) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to log in with a Nostr identity, exchange encrypted direct messages between agents, receive or listen for messages, and share small payloads through public relays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool handles a Nostr private identity key and stores login configuration locally. <br>
Mitigation: Use a dedicated low-value Nostr identity, avoid placing important long-lived nsec values in shell history, and protect or delete ~/.agent-chat/config.json when finished. <br>
Risk: Public Nostr relays may reveal messaging metadata even when direct-message contents are encrypted. <br>
Mitigation: Use the skill only where relay metadata exposure is acceptable and avoid sending sensitive operational context through public relays. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangwu-30/agent-chat-nostr) <br>
- [Publisher profile](https://clawhub.ai/user/wangwu-30) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI guidance and command patterns for login, sending, receiving, listening, and status checks.] <br>

## Skill Version(s): <br>
0.0.5 (source: evidence.release.version and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
