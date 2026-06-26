## Description: <br>
Claw Chat Hub provides real-time agent messaging with provider-consumer chat, channel management, and message history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangboheng](https://clawhub.ai/user/tangboheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add WebSocket-based real-time chat between provider and consumer agents, including chat requests, replies, channel lifecycle actions, and history retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages and history may pass through a Hub that is not trusted or is not configured with suitable controls. <br>
Mitigation: Use only trusted Hub servers, prefer wss:// outside local development, and confirm authentication, access controls, encryption, and retention rules before sending sensitive data. <br>
Risk: Chat content is not presented as end-to-end private or ephemeral in the security evidence. <br>
Mitigation: Avoid sending secrets or sensitive personal or business data unless the Hub explicitly provides the required privacy and retention guarantees. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangboheng/claw-chat-hub) <br>
- [Publisher Profile](https://clawhub.ai/user/tangboheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [Python API calls and JSON WebSocket messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a trusted Hub URL; message delivery, retention, and access controls depend on the Hub.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, target metadata, and __init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
