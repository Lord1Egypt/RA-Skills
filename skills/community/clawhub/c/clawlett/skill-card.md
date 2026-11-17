## Description:

Clawlett lets agents preview and, with explicit user confirmation, execute token swaps and Trenches token creation or trading on Base Mainnet through a Gnosis Safe and Zodiac Roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xardi](https://clawhub.ai/user/0xardi)

### License/Terms of Use:


## Use Case:

Developers and crypto operators use Clawlett to give an agent constrained access to quote balances, prepare swaps through KyberSwap or CoW Protocol, and manage Trenches token workflows from a Safe on Base Mainnet. The skill is intended for workflows where on-chain execution is explicitly confirmed by the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that the Trenches trading script can execute irreversible on-chain transactions without the documented execution flag or slippage protection.

Mitigation: Review carefully before installation, use only small disposable amounts, and require an explicit execution flag, nonzero minimum outputs, and exact token-address confirmations before using larger funds.

Risk: The wallet configuration directory contains an agent private key and may contain backend session cookies.

Mitigation: Restrict access to the configuration directory, avoid sharing generated config files, and rotate or reinitialize credentials if the directory is exposed.

Risk: On-chain actions depend on the Safe and Zodiac Roles permissions being configured as intended.

Mitigation: Verify the Safe owner, role key, scoped helper contracts, and allowed execution paths before funding the Safe or approving token operations.

## Reference(s):

- [Clawlett Skill Page](https://clawhub.ai/0xardi/skills/clawlett)
- [Publisher Profile](https://clawhub.ai/user/0xardi)
- [SKILL.md](artifact/SKILL.md)
- [Migration Guide](artifact/MIGRATION_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include quote previews, transaction commands, balance reports, migration guidance, and setup configuration details.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
