## Description: <br>
Send and receive P2P messages using disposable PINs. No servers, no accounts. For agent-to-agent messaging, approval flows, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EijiAC24](https://clawhub.ai/user/EijiAC24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate a disposable P2P messenger for agent-to-agent notifications, approval flows, and JSON stdin/stdout messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive chats, PINs, contacts, queued messages, and recovery information are stored under ~/.0x0. <br>
Mitigation: Review local storage behavior before installing and avoid sending secrets through pipe, listen, or chat workflows unless that storage model is acceptable. <br>
Risk: The scanner reports under-disclosed server behavior and says not to treat the tool as no-trace or server-free. <br>
Mitigation: Assess network behavior before use and avoid relying on the no-server claim for sensitive communications. <br>
Risk: The web UI can be exposed on the local network with --lan. <br>
Mitigation: Use --lan only on trusted networks and stop the web UI when it is not needed. <br>
Risk: Long-lived or public PINs can increase exposure for unsolicited or stale messages. <br>
Mitigation: Prefer short-lived or one-time PINs, revoke PINs when workflows finish, and review public PIN request handling. <br>


## Reference(s): <br>
- [0x0 Messenger README](artifact/README.md) <br>
- [0x0 homepage](https://0x0.contact) <br>
- [Hyperswarm](https://github.com/holepunchto/hyperswarm) <br>
- [ClawHub skill page](https://clawhub.ai/EijiAC24/0x0-messenger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and the c0x0 CLI binary.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
