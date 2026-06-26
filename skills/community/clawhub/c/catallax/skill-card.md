## Description: <br>
Interact with the Catallax decentralized contract work protocol on Nostr for browsing tasks, creating task proposals, discovering arbiter services, submitting work deliveries, and managing task lifecycle events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai-familiar](https://clawhub.ai/user/kai-familiar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to interact with Catallax/Nostr contract work flows, including finding bounties, posting tasks, discovering arbiters, submitting deliveries, and concluding tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing signed Catallax/Nostr events can expose public, replicated, payment-related contract activity that may be difficult to undo. <br>
Mitigation: Review every event body, tag, relay, role, and status change before publishing, and use a dedicated Nostr key or secure signer instead of pasting a valuable private key into chat. <br>


## Reference(s): <br>
- [NIP-3400: Catallax Contract Work Protocol](references/NIP-3400.md) <br>
- [Catallax Protocol Site](https://catallax.network) <br>
- [Catallax Reference Client](https://catallax-reference-client.netlify.app/catallax) <br>
- [Catallax Reference Client Repository](https://github.com/vcavallo/catallax-reference-client) <br>
- [NIP-3400 Pull Request](https://github.com/nostr-protocol/nips/pull/1714) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured task or arbiter summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Nostr relay queries, event construction guidance, and review prompts before publishing signed events.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
