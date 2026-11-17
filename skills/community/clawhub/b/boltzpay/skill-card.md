## Description:

Pay for API data automatically - multi-protocol (x402 + L402 + MPP), multi-chain, streaming sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leventilo](https://clawhub.ai/user/leventilo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use BoltzPay to discover paid API endpoints, quote prices, diagnose endpoints, and fetch API data through payment-enabled CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an unpinned remote npm CLI while using payment and wallet credentials.

Mitigation: Use a pinned and reviewed CLI version in an isolated environment before giving an agent payment credentials.

Risk: The default budget can be unlimited, which may allow unintended spend during paid API fetches.

Mitigation: Set a strict daily budget and require explicit approval before running `fetch` against any endpoint.

Risk: Payment credentials and wallet secrets may expose funds or unrelated accounts if reused broadly.

Mitigation: Use dedicated low-balance or test credentials and avoid exposing unrelated wallet, Lightning, Coinbase, or Stripe secrets.

## Reference(s):

- [BoltzPay ClawHub Skill Page](https://clawhub.ai/leventilo/skills/boltzpay)
- [BoltzPay Documentation](https://boltzpay.ai)
- [BoltzPay Registry](https://status.boltzpay.ai)
- [BoltzPay npm SDK](https://www.npmjs.com/package/@boltzpay/sdk)
- [Coinbase CDP Portal](https://portal.cdp.coinbase.com)
- [BoltzPay GitHub Link from Skill Documentation](https://github.com/leventilo/boltzpay)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and returned API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger paid API requests when the fetch command is used with payment credentials.]

## Skill Version(s):

0.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
