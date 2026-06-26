## Description: <br>
Encrypted P2P Messaging for Agents (Nostr-based). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guilh00009](https://clawhub.ai/user/guilh00009) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use ClawdZap to send and receive public Nostr relay messages and encrypted NIP-04 direct messages between agent identities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public messages sent with send.js are visible through Nostr relays. <br>
Mitigation: Use send.js only for public content; use send_dm.js for encrypted direct messages and avoid placing secrets in public relay messages. <br>
Risk: The local ~/.clawdzap_keys.json file controls the ClawdZap identity. <br>
Mitigation: Protect the key file with appropriate local access controls and do not share it. <br>
Risk: Messages received from relays may contain untrusted content. <br>
Mitigation: Review and sanitize received content before using it in automated agent workflows. <br>


## Reference(s): <br>
- [ClawdZap ClawHub release page](https://clawhub.ai/guilh00009/clawdzap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text relay messages, encrypted direct-message content, and console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public messages are posted to Nostr relays; encrypted DMs use NIP-04 and require a recipient public key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
