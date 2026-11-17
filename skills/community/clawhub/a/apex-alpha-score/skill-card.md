## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns APEX proprietary alpha score for current market opportunity quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers can call APEX Runner's paid market signal endpoint to retrieve an alpha score and rank opportunities. The skill presents the score as an input to trade entry decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured EVM private key can authorize USDC payments for endpoint calls.

Mitigation: Use a dedicated wallet with a limited balance, keep its key private, and retain the example's maximum-payment policy.

Risk: The skill describes the score as an entry gate for significant trades, so an agent could over-rely on a single paid signal.

Mitigation: Treat the score as one input and validate it against independent research and the user's trading criteria.

## Reference(s):

- [APEX Alpha Score endpoint](https://apexrunner.ai/signals/apex-alpha-score)
- [APEX Combined Alpha signal](https://apexrunner.ai/signals/combined-alpha)
- [APEX Agent Conviction Score signal](https://apexrunner.ai/signals/agent-conviction-score)
- [APEX Runner](https://apexrunner.ai)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Guidance]

**Output Format:** [Markdown instructions with a Python x402 request example and a JSON signal response.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid request; the example response includes alpha_score, percentile, signal_count, and confidence.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
