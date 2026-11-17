## Description:

Guide users on how to use the Batch EVM Address Balance Query API (/api/x402/batch-balance). Use when users ask about batch balance queries, multicall balance lookups, or how to call the x402-protected balance endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare paid x402 requests for querying native or ERC-20 balances across batches of EVM addresses. It provides request structure, shell commands, and code examples for the cpbox batch-balance endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to make automatic paid x402 API requests using wallet credentials.

Mitigation: Use a dedicated low-value wallet and require confirmation of payment amount, network, and recipient before sending requests.

Risk: The CLI example uses an unpinned npx package in a wallet-enabled workflow.

Mitigation: Prefer a pinned, reviewed package version or a controlled local install before use in sensitive workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-batch-balance)
- [Publisher profile](https://clawhub.ai/user/sprintmint)
- [Batch balance endpoint](https://www.cpbox.io/api/x402/batch-balance)
- [API provider](https://www.cpbox.io)
- [Payment facilitator](https://www.cppay.finance)
- [x402-payment wallet configuration](https://github.com/springmint/x402-payment#wallet-configuration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paid API request examples that require wallet configuration and x402 payment handling.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
