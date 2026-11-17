## Description:

Guides agents in using Foundry cast to read Ethereum on-chain state without wallet management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byron-mckeeby](https://clawhub.ai/user/byron-mckeeby)

### License/Terms of Use:


## Use Case:

Developers and blockchain operators use this skill to inspect Ethereum blocks, contract state, event logs, ENS records, and ABI data through read-only command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide asks users to run a remote Foundry installer.

Mitigation: Review and trust the upstream source before installation, and prefer a pinned and verified installation method.

Risk: One shell example builds a command string and executes it with eval, which can execute injected shell content.

Mitigation: Avoid copying the eval-based function as written; pass arguments directly or validate and quote all user-controlled inputs.

Risk: ABI lookup and ENS examples can disclose queried selectors, events, names, addresses, or profile fields to RPC providers and 4byte.directory.

Mitigation: Use trusted providers, avoid querying sensitive targets when privacy matters, and document which external services receive lookup data.

## Reference(s):

- [Foundry](https://foundry.paradigm.xyz)
- [4byte Directory signatures API](https://www.4byte.directory/api/v1/signatures/?hex_signature=0x$selector)
- [4byte Directory event signatures API](https://www.4byte.directory/api/v1/event-signatures/?hex_signature=0x$event_sig)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read-only Ethereum RPC examples that may require external RPC provider configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
