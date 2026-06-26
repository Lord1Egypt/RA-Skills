## Description: <br>
Derive Nostr identity (npub/nsec) from Archon DID. Use when unifying DID and Nostr identities so both use the same secp256k1 key. Requires existing Archon wallet with ARCHON_PASSPHRASE set. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macterra](https://clawhub.ai/user/macterra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators with an existing Archon wallet use this skill to derive and verify a Nostr keypair from the same secp256k1 key used by their Archon DID, then save the key and publish related identity metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally derives a Nostr identity from the same key material used by an Archon DID, so compromise of the Nostr secret can affect the unified identity. <br>
Mitigation: Install only when shared Archon and Nostr identity is intended; treat the nsec as full account ownership and store it in a secure secret manager or tightly permissioned file. <br>
Risk: The release security summary flags under-scoped secret handling for wallet-derived private keys. <br>
Mitigation: Run only on a trusted machine, avoid exposing terminal output or shell history, and review generated key storage permissions before using the identity. <br>
Risk: The release security guidance flags unpinned downloaded code and recommends avoiding curl-to-shell where possible. <br>
Mitigation: Audit or pin dependencies and installer sources before execution, and review DID updates or relay publications before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macterra/archon-nostr) <br>
- [nak installer referenced by the skill](https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Nostr nsec, npub, and hex public key values; the nsec is sensitive account-control material.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
