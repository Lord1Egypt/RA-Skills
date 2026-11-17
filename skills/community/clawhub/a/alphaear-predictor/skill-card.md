## Description:

Market prediction skill using Kronos. Use when user needs finance market time-series forecasting or news-aware finance market adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance analysts use this skill to generate Kronos-based market time-series forecasts and adjust them with recent news context. It supports workflows that need base OHLC-style forecasts plus a structured rationale for news-aware adjustments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe model-checkpoint loading can run code if an untrusted .pt checkpoint is placed under exports/models.

Mitigation: Use only controlled model directories, do not place untrusted checkpoints under exports/models, and prefer loaders that require weights_only=True or a non-executable model format.

Risk: The skill caches stock, search, news, and signal data locally.

Mitigation: Run it in an environment where local cache contents are acceptable for the data being processed, and clear or isolate the cache when handling sensitive workflows.

Risk: The skill can make outbound calls to market data, search, model, and configured LLM providers.

Mitigation: Review configured providers and API keys before use, and restrict network access in deployment environments that require tighter data-control boundaries.

## Reference(s):

- [AlphaEar Predictor prompts](references/PROMPTS.md)
- [ClawHub skill page](https://clawhub.ai/zhouzhonglu8-png/skills/alphaear-predictor)
- [BSQ paper](https://arxiv.org/pdf/2406.07548.pdf)
- [Soft entropy paper](https://arxiv.org/pdf/1911.05894.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and strict JSON forecast-adjustment output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast adjustment output is expected to include adjusted OHLCV points and a rationale.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
