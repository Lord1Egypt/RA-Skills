## Description:

Builds reviewable unsigned DeFi transaction plans with verified identities, ordered calls, explicit limits and unresolved prerequisites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi users use this skill to prepare and review bounded, unsigned transaction sequences before passing unchanged payloads to an authorized wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wrong target, spender, amount, chain or deadline in an unsigned plan could become financially binding if later approved or signed.

Mitigation: Review every generated target, calldata, approval, spender, amount, chain, deadline and warning before using a wallet.

Risk: Stale quotes or guessed outputs from dependent steps can make subsequent calls incorrect.

Mitigation: Use fresh state and actual received assets to rebuild dependent calls; verify the complete sequence before handoff.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/galleonlabs/skills/galleon-defi-agent-plan)
- [Official builders and capability boundaries](references/builders.md)
- [Worked unsigned plans](references/examples.md)
- [Aave MCP documentation](https://aave.com/docs/mcp/getting-started)
- [Nethermind DeFi skills documentation](https://github.com/NethermindEth/defi-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Unsigned transaction data, Guidance]

**Output Format:** [Markdown with ordered unsigned calls and prerequisites]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes chain and account identities, targets, calldata, amounts, limits, warnings and outstanding checks; does not sign or broadcast.]

## Skill Version(s):

0.1.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
