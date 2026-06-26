## Description: <br>
Use when claiming the AI bounty on the tDVV mainnet sidechain. First explain the difference between Portkey AA/CA and EOA, recommend AA/CA because the current campaign rewards 2 AIBOUNTY for AA/CA and 1 AIBOUNTY for EOA, then route to account onboarding, Portkey AA/CA claim through CA ManagerForwardCall, EOA claim, or diagnostics-only stop handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzz780](https://clawhub.ai/user/hzz780) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to choose and complete the supported AI bounty claim path on the aelf tDVV mainnet sidechain. It guides account selection, Portkey AA/CA and EOA claim routing, transaction confirmation, and diagnostic stop conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides wallet signing and on-chain writes, so a user could confirm the wrong signer, contract, receiver, reward, or gas assumptions. <br>
Mitigation: Before any write, show the signer, contract address, receiver semantics, reward amount, gas note, and transaction summary, then stop unless the user explicitly confirms. <br>
Risk: Wallet secrets could be exposed if a user pastes a seed phrase or private key into chat. <br>
Mitigation: Never request seed phrases or private keys; prefer an isolated or low-value wallet and rely on local wallet or Portkey account context. <br>
Risk: Exchange or custodial addresses cannot sign the required claim transaction and may cause failed or unsafe claim attempts. <br>
Mitigation: Stop when the address is exchange-managed, custodial, or not user-controlled, and continue only with a local EOA signer or resolved local AA/CA context. <br>
Risk: An unresolved Portkey AA/CA holder, caHash, recovery state, or tDVV account context can make the claim path invalid. <br>
Mitigation: Stop until holder and caHash resolution on tDVV, recovery, or local account readiness is complete; do not guess missing prerequisites. <br>


## Reference(s): <br>
- [AI Bounty Claim README](README.md) <br>
- [Account Choice And Onboarding](references/flows/account-choice.md) <br>
- [Diagnostics And Stop](references/flows/diagnostics-stop.md) <br>
- [EOA Claim](references/flows/eoa-skill.md) <br>
- [Portkey AA/CA Claim](references/flows/portkey-ca.md) <br>
- [Portkey EOA skill](https://github.com/Portkey-Wallet/eoa-agent-skills) <br>
- [Portkey CA skill](https://github.com/Portkey-Wallet/ca-agent-skills) <br>
- [tDVV chain status endpoint](https://tdvv-public-node.aelf.io/api/blockChain/chainStatus) <br>
- [ClawHub release page](https://clawhub.ai/hzz780/ai-bounty-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with transaction summaries, confirmation prompts, diagnostic stops, and optional shell or SDK command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction IDs and aelfscan tDVV lookup links after user-confirmed writes.] <br>

## Skill Version(s): <br>
2.10.0 (source: frontmatter); ClawHub release 0.1.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
