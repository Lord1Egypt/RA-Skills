## Description:

Binance Fiat request using the Binance API. Authentication requires API key and secret key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexploarer](https://clawhub.ai/user/dexploarer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Binance fiat deposit, withdrawal, payment history, and order detail endpoints with signed Binance API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Binance API credentials and server evidence flags broad secret-file searching and plaintext credential persistence.

Mitigation: Review before installing; use narrowly scoped Binance API keys, prefer IP allowlisting, disable withdrawals unless required, and do not let the skill store keys in TOOLS.md or read generic .env files containing unrelated secrets.

Risk: Mainnet fiat actions can create financial impact if executed without user intent.

Mitigation: Require explicit user confirmation before mainnet transactions and verify endpoint, account, and parameters before execution.

## Reference(s):

- [Binance Authentication](references/authentication.md)
- [Binance Fiat source homepage](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/fiat/SKILL.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Binance API credentials, signed request parameters, and the Binance Fiat API base URL.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
