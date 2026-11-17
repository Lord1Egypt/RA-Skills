## Description:

Local CLI tool for B.Fun (BSC) market inspection, quotes, token details, tax info, and explicitly user-confirmed token operations, with structured JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bfun-ai](https://clawhub.ai/user/bfun-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to inspect B.Fun markets on BSC, obtain quotes and token details, troubleshoot setup, and prepare explicitly confirmed token operations through the local bfun CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run mutable external CLI code with wallet signing access for on-chain actions.

Mitigation: Use a low-value dedicated wallet, avoid npx for secret-bearing workflows, prefer an exact reviewed package version or pinned commit, and provide PRIVATE_KEY only for intentional state-changing actions.

Risk: State-changing blockchain operations can cause irreversible asset loss if the token, amount, recipient, slippage, or chain is wrong.

Mitigation: Verify transaction details independently, require transaction-specific confirmation, and re-check BSC mainnet, token addresses, recipient addresses, amounts, and slippage before execution.

## Reference(s):

- [Token Phases](references/token-phases.md)
- [Trade Flow](references/trade-flow.md)
- [Create Flow](references/create-flow.md)
- [Contract Addresses](references/contract-addresses.md)
- [Common Errors](references/errors.md)
- [ClawHub Skill Page](https://clawhub.ai/bfun-ai/skills/bfun-agentic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only outputs can summarize CLI JSON; state-changing operations require transaction-specific user confirmation and local signing configuration.]

## Skill Version(s):

0.5.4 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
