## Description:

Send and receive P2P messages using disposable PINs. No servers, no accounts. For agent-to-agent messaging, approval flows, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eijiac24](https://clawhub.ai/user/eijiac24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation authors, and agents use this skill to set up disposable PIN-based peer-to-peer messaging, exchange notifications, run approval flows, and use JSON stdin/stdout channels for agent-to-agent communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web interface exposes sensitive messaging controls and metadata with too little authentication or disclosure.

Mitigation: Review before installing or running the web UI, keep the web UI bound to localhost, and avoid --lan on shared networks.

Risk: The local ~/.0x0 directory contains identity, PIN, contact, queue, and message data.

Mitigation: Treat ~/.0x0 as sensitive data, restrict local file access, and delete it when the messaging identity and history should be removed.

Risk: The notification feature should be treated as involving a centralized third-party endpoint until the publisher documents or removes it.

Mitigation: Avoid sharing sensitive content through notifications and require publisher documentation before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eijiac24/skills/0x0-messenger)
- [0x0 homepage](https://0x0.contact)
- [Hyperswarm](https://github.com/holepunchto/hyperswarm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and the c0x0 CLI; pipe mode emits newline-delimited JSON events.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
