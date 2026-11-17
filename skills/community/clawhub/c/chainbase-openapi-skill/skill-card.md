## Description:

Operate Chainbase indexed wallet and token reads through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure UXC and run read-only Chainbase wallet, token, and transaction data queries with API-key authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can load a changeable remote OpenAPI schema, so generated CLI behavior may differ from the reviewed package.

Mitigation: Prefer linking UXC to the bundled local schema or to an immutable, verified schema URL before running generated commands.

Risk: Wallet addresses, token contracts, and holder lookups are sent to Chainbase during API reads.

Mitigation: Use a Chainbase API key with the least privileges available and avoid broad wallet or token-holder crawls unless those queries are acceptable.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/chainbase-web3.openapi.json)
- [Remote curated OpenAPI schema](https://raw.githubusercontent.com/holon-run/uxc/main/skills/chainbase-openapi-skill/references/chainbase-web3.openapi.json)
- [Chainbase API key authentication docs](https://docs.chainbase.com/quickstart/authenticate-your-api-key)
- [Chainbase Web3 API balance docs](https://docs.chainbase.com/api-reference/web3-api/balance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Chainbase API operations through UXC; API responses use JSON envelopes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
