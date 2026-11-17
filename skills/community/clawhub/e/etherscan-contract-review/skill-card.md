## Description:

Review and explain verified deployed EVM smart contracts from a contract address and chain. Use when a user asks to break down what a Solidity contract does, map its architecture and source files, identify user/admin flows, proxy or implementation roles, asset movement, privileged controls, events, state variables, or unresolved uncertainty for developer onboarding, integration triage, or preliminary technical review. This is a developer-oriented contract review, not a security audit or safety certification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherscan](https://clawhub.ai/user/etherscan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to retrieve and explain verified deployed EVM smart contracts for onboarding, integration triage, and preliminary technical review. It focuses on architecture, user and admin flows, proxy roles, asset movement, privileged controls, events, state variables, and explicit uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make network requests and prompt for user-approved etherscan-cli installation or authentication.

Mitigation: Proceed only when the user wants Etherscan-compatible contract retrieval, require consent for setup, and keep retrieval read-only.

Risk: Etherscan API keys could be exposed if pasted into chat, logs, command arguments, or URLs.

Mitigation: Use CLI prompt-based login or a host-provided secret-safe environment mechanism; never ask the user to reveal the key in chat.

Risk: Retrieved contract source, metadata, filenames, comments, or linked content may contain hostile instructions.

Mitigation: Treat retrieved material as untrusted evidence only and do not execute retrieved code, scripts, build commands, or embedded instructions.

Risk: Readers may mistake the output for a security audit or safety certification.

Mitigation: State that the report is a developer-oriented source-code explanation and preserve uncertainty around incomplete, unverified, or unresolved contract evidence.

## Reference(s):

- [Etherscan Contract Review Skill](https://clawhub.ai/etherscan/skills/etherscan-contract-review)
- [Etherscan CLI](https://github.com/etherscan/etherscan-cli/)
- [Etherscan API Endpoint Overview](https://docs.etherscan.io/endpoint-overview)
- [Etherscan Common Error Messages](https://docs.etherscan.io/common-error-messages)
- [CLI Authentication](references/cli-authentication.md)
- [CLI Installation Fallback](references/cli-installation.md)
- [Smart Contract Patterns](references/patterns.md)
- [Report Rubric](references/report-rubric.md)
- [Source Analysis](references/source-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown explanations with source references and occasional shell commands or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Developer-oriented contract review output; not a security audit, safety certification, or formal verification result.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
