## Description:

Derive Nostr identity (npub/nsec) from Archon DID. Use when unifying DID and Nostr identities so both use the same secp256k1 key. Requires existing Archon wallet with ARCHON_PASSPHRASE set.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macterra](https://clawhub.ai/user/macterra)

### License/Terms of Use:


## Use Case:

Developers and technically advanced users use this skill to derive Nostr npub/nsec keys from an existing Archon DID wallet and document the linkage between their DID and Nostr profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles wallet mnemonic material and Nostr private keys.

Mitigation: Use only in an isolated environment, keep nsec values out of terminal logs and command arguments, and store secret key files with restrictive permissions.

Risk: The artifact recommends a curl|sh installer and installs npm dependencies dynamically.

Mitigation: Avoid the curl|sh installer where possible, and pin and audit dependencies before execution.

Risk: Publishing DID and profile data to Nostr relays can publicly link the user's Archon and Nostr identities.

Mitigation: Publish DID or profile data to relays only when that public linkage is intentional.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that output Nostr secret key material; handle generated nsec values as sensitive.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
