## Description:

Execute leverage trading on Avantis (Base). Long/short crypto, forex, commodities with up to 100x leverage. Uses Python SDK with direct wallet integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droppingbeans](https://clawhub.ai/user/droppingbeans)

### License/Terms of Use:

MIT

## Use Case:

External developers and trading operators use this skill to inspect Avantis positions and run long, short, and close-position workflows on Base through Python scripts. It is intended for leveraged trading and should be audited before live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet keys and live Base mainnet transactions.

Mitigation: Audit and modify the skill before installation, avoid plaintext private-key files, and use an external signer or minimally funded wallet for live trading.

Risk: The artifact includes wallet material and scripts that can approve USDC or open and close leveraged positions.

Mitigation: Remove and rotate any exposed wallet keys, do not reuse the shipped key, and add dry-run plus explicit confirmation gates before approvals or trades.

Risk: The skill depends on external trading SDK behavior for transaction construction and execution.

Mitigation: Pin and review dependencies before use and test changes with small amounts before allowing larger trades.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/droppingbeans/skills/avantis-skill)
- [Avantis Quick Start](references/quick-start.md)
- [Avantis Platform](https://avantisfi.com)
- [Avantis SDK Docs](https://sdk.avantisfi.com)
- [Avantis Trading Guide](https://docs.avantisfi.com)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, API Calls]

**Output Format:** [Markdown guidance with bash commands and transaction status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit live Base mainnet approvals and trades when its scripts are run with a funded wallet.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
