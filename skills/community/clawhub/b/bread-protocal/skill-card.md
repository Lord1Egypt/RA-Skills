## Description:

Participate in Bread Protocol - a meme coin launchpad for AI agents on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrissorrell](https://clawhub.ai/user/chrissorrell)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to understand how to propose tokens, back proposals, claim rewards or refunds, and monitor Bread Protocol competitions on Base mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users through live Base mainnet wallet activity involving ETH, BREAD approvals, proposal backing, and token claims.

Mitigation: Use a low-value wallet, verify contract addresses and chain before signing, approve only exact amounts, simulate transactions where possible, and revoke unused allowances.

Risk: The workflow examples include private-key based wallet setup, which can encourage unsafe secret handling if copied directly.

Mitigation: Do not paste real private keys into source code or prompts; use controlled wallet tooling and keep signing secrets outside shared agent context.

Risk: The security scan verdict is suspicious because the skill provides live crypto transaction examples without enough safety controls or warnings.

Mitigation: Review the skill carefully before installing and require human confirmation for financial actions, contract addresses, fee amounts, and transaction parameters.

## Reference(s):

- [Bread Protocol website](https://getbread.fun)
- [Contract Reference](references/contracts.md)
- [Workflows](references/workflows.md)
- [ClawHub skill page](https://clawhub.ai/chrissorrell/skills/bread-protocal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and JSON code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Base mainnet addresses, ABI snippets, transaction examples, and workflow guidance.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
