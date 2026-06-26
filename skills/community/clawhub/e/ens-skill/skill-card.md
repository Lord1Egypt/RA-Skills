## Description: <br>
Resolve ENS names (.eth) to Ethereum addresses and vice versa, look up ENS profiles, and help users register, renew, or manage .eth names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to resolve ENS names and wallet addresses, inspect ENS profile records, and guide .eth registration, renewal, and record-management workflows on Ethereum mainnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ENS names and wallet addresses may be queried through third-party services during resolution and profile lookup. <br>
Mitigation: Use the minimum lookup needed for the task, cache results only within the active session, and make users aware when third-party services are involved. <br>
Risk: ENS records can change, and an incorrect or stale resolution could route funds or updates to the wrong address. <br>
Mitigation: Before any transaction, show the resolved 0x address, chain, cost, and wallet prompt, and require explicit user confirmation. <br>
Risk: .eth registration, renewal, and record-management actions require Ethereum mainnet gas, fees, and contract interactions. <br>
Mitigation: Present the chain, estimated cost, and operation steps before approval, and direct first-time or complex workflows to the ENS Manager App. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fabriziogianni7/ens-skill) <br>
- [ENS documentation](https://docs.ens.domains/) <br>
- [ENS Manager App](https://ens.app/myname.eth) <br>
- [web3.bio profile API example](https://api.web3.bio/profile/vitalik.eth) <br>
- [ENS avatar metadata endpoint](https://metadata.ens.domains/mainnet/avatar/{name}) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference third-party ENS, web3.bio, The Graph, and Ethereum RPC services; registration, renewal, record updates, and transfers require user confirmation before wallet execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
