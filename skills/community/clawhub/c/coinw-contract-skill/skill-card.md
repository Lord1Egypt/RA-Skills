## Description:

Coinw Contract REST API skill: covers market data, order placement/cancellation, TP/SL, position and order queries, account assets, position modes, and leverage queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[connectcoinw](https://clawhub.ai/user/connectcoinw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to query CoinW futures market and account data, prepare signed CoinW contract API requests, and manage futures orders, TP/SL, positions, leverage, margin, and account assets.

### Deployment Geography for Use:

Global, subject to CoinW service availability and applicable digital-asset trading rules.

## Known Risks and Mitigations:

Risk: The skill can guide agents through futures trading actions such as placing, closing, reversing, and changing margin on positions.

Mitigation: Require explicit user confirmation before any order, close, reverse, TP/SL, leverage, or margin-changing action is executed.

Risk: The skill requires CoinW API credentials for private account and trading endpoints.

Mitigation: Use read-only keys where possible, never paste secrets into chat, keep withdrawal permission disabled, enable IP allowlisting, and apply least-privilege API permissions.

Risk: Incorrect authentication or request construction can fail private requests or create unintended account operations.

Mitigation: Use CoinW contract signing only, verify endpoint paths and request payloads before submission, and check returned order or position status after trading requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/connectcoinw/skills/coinw-contract-skill)
- [Authentication & Base URL](references/Authentication.md)
- [API Key Creation Steps](references/api-key-creation-steps.md)
- [Error Code Explanation](references/error-codes.md)
- [CoinW Futures Notes](references/notes.md)
- [CoinW Futures Instrument Information](https://www.coinw.com/api-doc/futures-trading/market/get-instrument-information)
- [CoinW Futures Place Order](https://www.coinw.com/api-doc/futures-trading/trade/place-an-order)
- [CoinW Futures Current Positions](https://www.coinw.com/api-doc/futures-trading/position/get-current-position-information)
- [CoinW Futures Account Assets](https://www.coinw.com/api-doc/futures-trading/assets/get-futures-account-assets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown API reference with endpoint tables, credential setup notes, and bash/curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private endpoints require CoinW API credentials, millisecond timestamps, and HMAC-SHA256 Base64 signatures.]

## Skill Version(s):

1.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
