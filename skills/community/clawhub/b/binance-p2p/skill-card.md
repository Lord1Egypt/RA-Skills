## Description:

Binance P2P trading assistant for checking P2P prices, advertisements, payment methods, and personal P2P order history, excluding spot, futures, and exchange trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexploarer](https://clawhub.ai/user/dexploarer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Binance P2P market quotes and ads, compare payment methods, and summarize personal P2P order history when read-only Binance API credentials are supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Binance API credentials for personal order history.

Mitigation: Use read-only API keys, enable IP allowlisting where possible, and provide secrets through a secure runtime mechanism rather than committed files.

Risk: The artifact includes a Bash authentication example that could expose real credentials if copied directly with live keys.

Mitigation: Keep example values as placeholders, avoid placing real keys in command arguments or shared shell history, and prefer an in-process client or secret manager.

Risk: Incorrect credential scope could allow actions beyond order-history lookup.

Mitigation: Enable only Binance reading permission and avoid trading, withdrawal, modification, or advertisement-management permissions.

## Reference(s):

- [Authentication reference](references/authentication.md)
- [ClawHub skill page](https://clawhub.ai/dexploarer/skills/binance-p2p)
- [Binance public API host](https://www.binance.com)
- [Binance SAPI host](https://api.binance.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request guidance, concise lists or tables, and optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Binance endpoint parameters, read-only credential setup guidance, and UTC-formatted order summaries; does not support automated order placement.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
