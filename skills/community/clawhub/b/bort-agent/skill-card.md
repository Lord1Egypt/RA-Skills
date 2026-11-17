## Description:

Interact with BORT AI agents on BNB Chain via BAP-578 by sending messages, checking runtime status, and querying on-chain agent identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsu-j](https://clawhub.ai/user/tsu-j)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to interact with BORT WebAPI agents, check agent connection health, and verify BAP-578 NFT agent identity on BNB Smart Chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages sent through the skill leave the local environment for the configured BORT runtime.

Mitigation: Verify BORT_RUNTIME_URL before use and do not send credentials, wallet secrets, tokens, personal data, or confidential material.

Risk: BNB_RPC_URL controls where on-chain identity queries are sent.

Mitigation: Use a trusted BNB Smart Chain RPC endpoint and verify the destination before running query commands.

Risk: The optional author argument may be unsafe with quotes or structured text.

Mitigation: Use a simple sender identifier until the author value is JSON-escaped properly.

## Reference(s):

- [BAP-578 Overview](references/bap578-overview.md)
- [BAP-578 Contract on BSCScan](https://bscscan.com/address/0x15b15df2ffff6653c21c11b93fb8a7718ce854ce)
- [Platform Registry on BSCScan](https://bscscan.com/address/0x985eae300107a838c1aB154371188e0De5a87316)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured BORT runtime and BNB RPC endpoints; command outputs depend on the selected agent ID and endpoint responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
