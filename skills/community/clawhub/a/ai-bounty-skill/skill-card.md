## Description:

Guides agents through AI bounty claims on the aelf tDVV sidechain, routing users between Portkey AA/CA, EOA, onboarding, and diagnostics flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzz780](https://clawhub.ai/user/hzz780)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through choosing AA/CA or EOA and preparing an AI bounty claim on tDVV while stopping on custody, fee, recovery, RPC, or transaction blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-related dependencies are unpinned, so dependency changes could alter signing or transaction behavior.

Mitigation: Install only after review, and pin the Portkey EOA and CA dependencies to reviewed commits or otherwise verified releases.

Risk: Example behavior includes raw manager private-key handling for a blockchain transaction path.

Mitigation: Prefer a signer interface that never exposes key material, and avoid asking users to paste or reveal private keys.

Risk: An on-chain write can target the wrong receiver, chain, contract, method, fee condition, or reward amount if details are not checked.

Mitigation: Confirm decoded transaction details, receiver semantics, chain, contract, fee status, and reward amount before any send.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hzz780/skills/ai-bounty-skill)
- [README](README.md)
- [Account choice flow](references/flows/account-choice.md)
- [Portkey AA/CA claim flow](references/flows/portkey-ca.md)
- [EOA claim flow](references/flows/eoa-skill.md)
- [Diagnostics and stop flow](references/flows/diagnostics-stop.md)
- [Portkey EOA skill dependency](https://github.com/Portkey-Wallet/eoa-agent-skills)
- [Portkey CA skill dependency](https://github.com/Portkey-Wallet/ca-agent-skills)
- [tDVV RPC chain status](https://tdvv-public-node.aelf.io/api/blockChain/chainStatus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown responses with claim routing guidance, transaction summaries, diagnostic stop messages, and occasional TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before on-chain writes and should surface transaction IDs, final chain results, and exact chain errors when available.]

## Skill Version(s):

0.1.1 (source: server release metadata; bundled SKILL.md declares behavior version 2.10.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
