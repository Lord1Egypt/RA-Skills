## Description:

AI-generated market narrative based on current regime and data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use Ai Narrative to fetch a paid real-time market narrative for macro context, reasoning summaries, and strategy preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to use a raw EVM private key for automatic wallet-funded requests without clear per-call confirmation or spending controls.

Mitigation: Use a dedicated low-balance wallet, confirm the expected price before use, and avoid unattended repeated invocations unless external spending limits and key rotation are in place.

Risk: The skill provides paid market-signal context that could influence trading decisions.

Mitigation: Treat responses as contextual market information and require human or policy review before executing trading strategies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/ai-narrative)
- [APEX Runner Ai Narrative Signal](https://apexrunner.ai/signals/ai-narrative)
- [APEX Runner Pricing Check](https://apexrunner.ai/signals/my-pricing)
- [Narrative Intelligence Signal](https://apexrunner.ai/signals/narrative-intelligence)
- [Whale Sentiment Signal](https://apexrunner.ai/signals/whale-sentiment)
- [Regime Signal](https://apexrunner.ai/signals/regime)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON response and agent-facing text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an EVM wallet private key and wallet-funded x402 requests to the signal endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
