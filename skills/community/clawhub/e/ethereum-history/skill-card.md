## Description:

Ethereum History provides read-only factual data about historical Ethereum mainnet contracts, including deployment details, bytecode, decompiled code, metadata, links, and documented historical context when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cartoonitunes](https://clawhub.ai/user/cartoonitunes)

### License/Terms of Use:


## Use Case:

Developers, analysts, and researchers use this skill to look up historical Ethereum mainnet contract facts by address, era, timestamp range, deployer, bytecode availability, or documentation status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to query ethereumhistory.com or a configured BASE_URL.

Mitigation: Confirm the intended endpoint before use and keep requests read-only.

Risk: Returned bytecode or decompiled code may be misunderstood as executable guidance.

Mitigation: Treat returned bytecode and decompiled code as reference data, not code to execute.

## Reference(s):

- [Ethereum History](https://ethereumhistory.com)
- [Ethereum History Agent Manifest](https://ethereumhistory.com/api/agent/manifest)
- [ClawHub Skill Page](https://clawhub.ai/cartoonitunes/skills/ethereum-history)
- [Publisher Profile](https://clawhub.ai/user/cartoonitunes)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, markdown]

**Output Format:** [Markdown guidance with GET request examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned contract data can include runtime bytecode and decompiled code as reference data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
