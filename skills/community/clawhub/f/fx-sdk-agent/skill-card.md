## Description:

Use FX Protocol TypeScript SDK (fx-sdk) to query positions, build leverage operation transaction plans, bridge tokens between Base and Ethereum, and generate runnable scripts for FX Protocol and fxSAVE workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huwangtao123](https://clawhub.ai/user/huwangtao123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate @aladdindao/fx-sdk into agents or tools, generate transaction-planning code, debug SDK parameters, and validate FX Protocol workflows on Ethereum mainnet or Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated blockchain transaction code can move funds or approve token spending if executed without review.

Mitigation: Keep generated code in dry-run or plan-only mode until the user manually checks chain, recipient, token, amount, approvals, slippage, and gas costs.

Risk: FX Protocol workflows involve leveraged trading, smart contracts, bridging, and volatile crypto markets.

Mitigation: Require explicit confirmation before broadcasting wallet transactions and review SDK routes, transaction order, and post-execution balance or position checks.

## Reference(s):

- [FX SDK repository](https://github.com/aladdindao/fx-sdk.git)
- [FX SDK skill repository](https://github.com/AladdinDAO/fx-sdk-skill.git)
- [f(x) Protocol website](https://fx.aladdin.club/)
- [FX SDK Agent references](references/README.md)
- [FX SDK Playbook](references/sdk-playbook.md)
- [Agent adapter example](references/agent-adapter-example.ts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript code blocks, shell commands, transaction plan descriptions, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated transaction code should remain in dry-run or plan-only mode until the user manually verifies chain, recipient, token, amount, approvals, slippage, and gas costs.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
