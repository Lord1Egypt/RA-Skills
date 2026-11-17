## Description:

Command-line Nostr client for agent-to-agent encrypted messaging, identity login, realtime listening, and small file sharing through public Nostr relays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwu-30](https://clawhub.ai/user/wangwu-30)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to configure a Nostr identity, send and receive encrypted direct messages, run a resident listener, and exchange small files over public relays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The login flow accepts a long-lived Nostr private key on the command line and persists it in plaintext under the user's home directory.

Mitigation: Use a dedicated low-value Nostr key for this skill, avoid primary identities, restrict local file access, and remove the saved config when the skill is no longer needed.

Risk: Messages use public Nostr relays, so relay metadata and small file events may be visible to relay operators and recipients.

Mitigation: Send only content suitable for the configured relays, verify recipient public keys before sending, and avoid sharing sensitive files through relay events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangwu-30/skills/agent-chat-nostr)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Nostr npub/nsec identity inputs and public relay configuration.]

## Skill Version(s):

0.0.5 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
