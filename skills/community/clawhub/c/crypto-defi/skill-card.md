## Description:

Crypto Defi helps agents record, review, search, and export local plaintext notes about DeFi positions, portfolio snapshots, price observations, gas fees, whale activity, and protocol analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill as a local crypto activity logbook for tracking DeFi positions, portfolio notes, alerts, market observations, and exports. It should not be treated as an automated yield calculator or financial advice source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores crypto notes in plaintext local log files, which may expose sensitive balances, strategies, or wallet-related observations to anyone with filesystem access.

Mitigation: Avoid entering wallet secrets, seed phrases, private keys, exact balances, or sensitive trading strategy; restrict permissions on ~/.local/share/crypto-defi before use.

Risk: The advertised DeFi yield-calculator positioning does not match the inspected artifact's local logbook behavior.

Mitigation: Use the skill only for recording and reviewing user-provided observations, and independently validate any yield, APY, impermanent-loss, staking, or investment analysis.

## Reference(s):

- [Crypto Defi ClawHub listing](https://clawhub.ai/xueyetianya/skills/crypto-defi)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plaintext command output with local plaintext logs and optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered records under ~/.local/share/crypto-defi and does not require API keys or network access.]

## Skill Version(s):

2.4.9 (source: ClawHub release evidence; artifact frontmatter and script report v2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
