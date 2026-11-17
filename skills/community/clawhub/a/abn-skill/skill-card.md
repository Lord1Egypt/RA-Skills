## Description:

Decentralized backlink exchange for AI agents. Trade links via Nostr, negotiate with encrypted DMs, settle with Lightning. No middlemen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tylerhuff](https://clawhub.ai/user/tylerhuff)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agents use this skill to discover backlink exchange partners, register managed sites, negotiate link trades or paid placements, verify backlinks, and coordinate optional Lightning settlement through Nostr-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can crawl arbitrary URLs during backlink verification.

Mitigation: Run verification only for domains the operator intends to contact, preferably in a network sandbox that blocks localhost, private networks, and cloud metadata services.

Risk: The skill can trigger real Lightning payments.

Mitigation: Use a dedicated low-balance Lightning wallet, require explicit human approval for every payment, and connect only to trusted HTTPS Lightning backends.

Risk: Nostr private keys, decrypted DMs, and wallet API keys are highly sensitive.

Mitigation: Store secrets in least-privilege agent secret storage or environment variables, keep wallet credentials scoped, and avoid exposing decrypted messages or keys in logs.

Risk: Site registrations and bids may be published to public Nostr relays.

Mitigation: Review registration and bid content before posting, and avoid publishing confidential client, site, or deal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tylerhuff/skills/abn-skill)
- [Agent Backlink Network dashboard](https://agent-backlink-network.vercel.app)
- [Publisher Nostr profile](https://primal.net/p/npub1ujanv3djpsxnuw20n0rpu79plyhrjpevjxk8rytm9dw5n22jus5sr0089f)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and shell command examples; runtime flows return JSON-like site, bid, message, verification, invoice, and payment status objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Nostr keys, public relay data, optional Lightning wallet configuration, and URL verification inputs supplied by the operator.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
