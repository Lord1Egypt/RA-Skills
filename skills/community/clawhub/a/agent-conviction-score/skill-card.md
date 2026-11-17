## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns measures conviction strength of current APEX trade signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use the endpoint to retrieve an APEX conviction score when comparing trade setups or considering signal strength for position sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls make paid USDC transactions, and the example signs requests using EVM_PRIVATE_KEY.

Mitigation: Keep the key in a protected environment variable and set a strict x402 payment cap before making requests.

Risk: The security review scanned one Markdown component and does not establish behavior outside that scanned scope.

Mitigation: Review the endpoint integration and runtime behavior before using it with a funded wallet.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/agent-conviction-score)
- [APEX Runner conviction score endpoint](https://apexrunner.ai/signals/agent-conviction-score)
- [APEX Runner apex-alpha-score](https://apexrunner.ai/signals/apex-alpha-score)
- [APEX Runner signal-intelligence](https://apexrunner.ai/signals/signal-intelligence)
- [APEX Runner crowded-trade-detector](https://apexrunner.ai/signals/crowded-trade-detector)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code]

**Output Format:** [A JSON response with conviction, aligned-signal count, direction, and confidence; includes Markdown guidance and a Python request example.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an EVM private key and USDC on Base for paid calls.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
