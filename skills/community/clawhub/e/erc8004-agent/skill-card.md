## Description: <br>
ERC8004 Agent helps agents create or manage Ethereum wallet-backed ERC-8004 identities, register onchain, maintain registration metadata, and authenticate through SIWA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limone-eth](https://clawhub.ai/user/limone-eth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up ERC-8004 onchain agent identities, prepare registration metadata, operate a keyring proxy, and complete SIWA authentication flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent wallet-signing capability for SIWA messages and onchain transactions. <br>
Mitigation: Use a fresh low-value wallet, prefer testnets during evaluation, and require explicit user approval before each signing operation or onchain transaction. <br>
Risk: The external SDK and keyring proxy are privileged signing dependencies. <br>
Mitigation: Audit or pin the SDK and proxy before production use, and run the keyring proxy as an isolated process with HMAC credentials kept out of shared memory. <br>
Risk: SIWA or JWT session tokens stored in MEMORY.md or shared agent memory could leak authentication state. <br>
Mitigation: Do not store SIWA or JWT session tokens in MEMORY.md or shared memory files; store only public identity state and redact tokens from logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/limone-eth/erc8004-agent) <br>
- [ERC-8004 registration guide](references/registration-guide.md) <br>
- [SIWA protocol specification](references/siwa-spec.md) <br>
- [ERC-8004 contract addresses and ABIs](references/contract-addresses.md) <br>
- [Security model](references/security-model.md) <br>
- [Registration template](assets/registration-template.json) <br>
- [Keyring proxy deployment guide](https://siwa.builders.garden/docs/deploy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash, TypeScript, Python, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include onchain transaction steps, public identity state updates, registration JSON, and SIWA authentication requests.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata; artifact frontmatter and package.json show 0.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
