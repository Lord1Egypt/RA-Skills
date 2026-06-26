## Description: <br>
Interact with BORT AI agents on BNB Chain via BAP-578 by sending messages, checking runtime status, and querying on-chain identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsu-j](https://clawhub.ai/user/tsu-j) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to communicate with BORT agents, check whether a runtime connector is healthy, and verify agent ownership or type on BNB Smart Chain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages are sent to a BORT runtime endpoint and external agent responses may be untrusted. <br>
Mitigation: Use only trusted BORT_RUNTIME_URL values, avoid sending sensitive information, and review returned agent content before relying on it. <br>
Risk: On-chain identity queries depend on the configured BNB Smart Chain RPC endpoint. <br>
Mitigation: Verify BNB_RPC_URL before use and treat RPC failures or unexpected empty responses as unresolved identity checks. <br>


## Reference(s): <br>
- [BAP-578 overview](references/bap578-overview.md) <br>
- [BAP-578 contract on BSCScan](https://bscscan.com/address/0x15b15df2ffff6653c21c11b93fb8a7718ce854ce) <br>
- [Platform Registry on BSCScan](https://bscscan.com/address/0x985eae300107a838c1aB154371188e0De5a87316) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [JSON responses from shell scripts with markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted BORT runtime endpoint for messaging and a BNB Smart Chain RPC endpoint for on-chain reads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
