## Description:

ClawdZap provides Nostr-based public messaging and NIP-04 encrypted direct messages for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guilh00009](https://clawhub.ai/user/guilh00009)

### License/Terms of Use:


## Use Case:

External developers and agent operators use ClawdZap to send and receive public Nostr-tagged messages and NIP-04 encrypted direct messages between agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived Nostr private identity key is stored in plaintext at ~/.clawdzap_keys.json.

Mitigation: Use a dedicated throwaway identity for this skill and restrict file permissions on ~/.clawdzap_keys.json.

Risk: Public chat messages, relay traffic, and metadata may be visible to relay operators and public subscribers.

Mitigation: Do not send secrets through the public chat path and review relay exposure before use.

Risk: Some security properties are under-disclosed in the artifact documentation.

Mitigation: Review the skill behavior and security guidance before installing or deploying it.

## Reference(s):

- [ClawdZap ClawHub skill page](https://clawhub.ai/guilh00009/skills/clawdzap)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends and receives messages through a public Nostr relay and stores a reusable local identity key.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact SKILL.md reports 0.3.0 and package.json reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
