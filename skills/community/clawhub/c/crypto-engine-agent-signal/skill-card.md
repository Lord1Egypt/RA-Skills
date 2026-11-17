## Description:

Buy the latest machine-readable BTC directional signal from Crypto Engine through a Tempo MPP-enabled endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weifenghuang](https://clawhub.ai/user/weifenghuang)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to purchase and retrieve a live BTC directional signal from Crypto Engine when their runtime supports Tempo MPP payments. It helps payment-capable agents return the signal direction, brief reason, and timestamp without inventing a fresh result when the paid API cannot be reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may complete a paid wallet transaction without a user-approved price cap.

Mitigation: Set wallet-side transaction limits and require explicit confirmation of the amount, currency, network, merchant, and endpoint before payment.

Risk: The runtime may be unable to satisfy the Tempo MPP payment challenge and still produce an unsupported signal.

Mitigation: Stop and report the limitation when payment support is unavailable or the API call fails; do not invent or cache a signal as fresh.

Risk: Wallet secrets or unrelated credentials could be exposed during the payment flow.

Mitigation: Use payment middleware that withholds seed phrases and unrelated credentials from the Crypto Engine endpoints.

## Reference(s):

- [Crypto Engine discovery document](https://cryptoengine.club/api)
- [Crypto Engine paid signal endpoint](https://cryptoengine.club/api/agent-signal)
- [Crypto Engine public AI index](https://cryptoengine.club/llms.txt)
- [Crypto Engine public skill instructions](https://cryptoengine.club/skills/crypto-engine-agent-signal/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/weifenghuang/skills/crypto-engine-agent-signal)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, JSON]

**Output Format:** [Markdown guidance with JSON API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns or summarizes direction, brief_reason, and signal_timestamp when the paid endpoint succeeds.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
