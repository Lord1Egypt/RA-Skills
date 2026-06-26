## Description: <br>
Register ENS names, create subdomains, and publish IPFS sites without manual contract calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zeugh-eth](https://clawhub.ai/user/Zeugh-eth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check ENS name status, register .eth names, create ENS subdomains, and set IPFS content hashes through command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to handle Ethereum wallet credentials, including keystore passwords and private keys. <br>
Mitigation: Use a fresh low-balance wallet, prefer protected keystore or environment-variable flows, and avoid command-line passwords and raw private keys. <br>
Risk: Generated workflows can submit real Ethereum mainnet ENS transactions and spend ETH. <br>
Mitigation: Run dry-runs first and manually verify the name, duration, chain, signer, recipient, and ETH cost before any write operation. <br>
Risk: Security evidence warns not to rely on the registration script until the keystore/account-binding issue is fixed. <br>
Mitigation: Avoid the registration script for funded wallets until that issue is remediated, and independently verify any account used to sign transactions. <br>


## Reference(s): <br>
- [ENS Basics](references/ens-basics.md) <br>
- [ENS Documentation](https://docs.ens.domains) <br>
- [ENS NameWrapper Guide](https://docs.ens.domains/wrapper/overview) <br>
- [ENS Public Resolver contenthash](https://docs.ens.domains/contract-api-reference/publicresolver#contenthash) <br>
- [eth.limo](https://eth.limo) <br>
- [ENS App](https://app.ens.domains) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger Ethereum mainnet reads and transactions when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter, CHANGELOG, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
