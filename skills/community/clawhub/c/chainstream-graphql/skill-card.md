## Description:

Executes flexible GraphQL queries against ChainStream's on-chain data warehouse for custom blockchain analytics, including cross-cube joins, aggregations, filters, and time-series analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harry5556](https://clawhub.ai/user/harry5556)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build and run custom ChainStream GraphQL analytics over blockchain data when standard REST or MCP endpoints are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable external CLI execution in workflows that may touch credentials, wallets, and paid subscription flows.

Mitigation: Run it in an isolated environment with a preinstalled, version-pinned ChainStream CLI; review commands before execution and avoid piping remote installers into a shell.

Risk: Authentication and payment flows can create wallets, store keys, import private keys, or purchase quota.

Mitigation: Require explicit user confirmation before wallet creation, key storage, private-key import, or any paid plan purchase; avoid high-value private keys.

## Reference(s):

- [ChainStream GraphQL Schema Guide](artifact/references/schema-guide.md)
- [ChainStream GraphQL Query Patterns](artifact/references/query-patterns.md)
- [ChainStream Authentication](artifact/shared/authentication.md)
- [ChainStream Payment Protocols](artifact/shared/x402-payment.md)
- [ChainStream Error Handling](artifact/shared/error-handling.md)
- [ChainStream Documentation](https://docs.chainstream.io)
- [ChainStream API Reference](https://docs.chainstream.io/api-reference)
- [ChainStream Dashboard](https://app.chainstream.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with GraphQL snippets, JSON-oriented CLI output, shell commands, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke live ChainStream CLI or MCP calls that require API credentials, subscription quota, and explicit confirmation for paid plan purchases.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
