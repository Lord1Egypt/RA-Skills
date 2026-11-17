## Description:

Clawlet helps an OpenClaw agent manage Nostr identities, publish posts, manage follows, read timelines, filter and recommend content, exchange NIP-04 direct messages, and manage contact nicknames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[6830920](https://clawhub.ai/user/6830920)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use Clawlet through OpenClaw to operate a Nostr identity: create keys, publish posts, manage follows, read and filter timelines, send encrypted direct messages, and manage nicknames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-controlling Nostr private keys may be stored or exported in plaintext.

Mitigation: Use only throwaway or low-value Nostr identities until encrypted key storage, keychain integration, and explicit confirmation for key export are added.

Risk: When authenticated user context is missing, the skill may fall back to a shared default identity.

Mitigation: Require authenticated user context and a bound identity before posting, following, exporting keys, or sending direct messages.

Risk: Posts, follows, and direct-message metadata can be visible to Nostr relays even when message content is encrypted.

Mitigation: Add confirmations for network-visible actions, warn users about observable metadata, and verify relay event responses.

Risk: The security evidence recommends review before installation and dependency lockfile refresh.

Mitigation: Install in an isolated environment, review dependencies and configured relays, and refresh the lockfile before trusted use.

## Reference(s):

- [Clawlet ClawHub listing](https://clawhub.ai/6830920/skills/clawlet)
- [Clawlet project homepage](https://github.com/openclaw/clawlet)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON-like skill results and text messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish to or read from configured Nostr relays as a side effect of user-requested actions.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
