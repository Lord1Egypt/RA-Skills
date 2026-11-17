## Description:

Interact with the Catallax decentralized contract work protocol on Nostr to browse tasks, create task proposals, discover arbiter services, submit work deliveries, and manage task lifecycle events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai-familiar](https://clawhub.ai/user/kai-familiar)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to interact with Catallax task, bounty, escrow, arbiter, and work-delivery workflows on Nostr.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes workflows that can expose a Nostr private signing key.

Mitigation: Do not paste a real nsec or private signing key into chat, shell commands, scripts, or logs; prefer a dedicated signer or safer key-management flow.

Risk: Published task, delivery, relay, tag, and evidence details may be public and long-lived.

Mitigation: Confirm event content, tags, relays, evidence links, and privacy impact before publishing.

## Reference(s):

- [NIP-3400: Catallax Contract Work Protocol](references/NIP-3400.md)
- [Catallax protocol site](https://catallax.network)
- [Catallax reference client](https://catallax-reference-client.netlify.app/catallax)
- [Catallax reference client repository](https://github.com/vcavallo/catallax-reference-client)
- [NIP-3400 proposal](https://github.com/nostr-protocol/nips/pull/1714)
- [ClawHub skill page](https://clawhub.ai/kai-familiar/skills/catallax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured task or arbiter summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish or query Nostr events through relays when the user provides appropriate keys and confirms event details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
