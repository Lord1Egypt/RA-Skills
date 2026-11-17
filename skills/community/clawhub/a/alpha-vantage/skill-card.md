## Description:

Use this skill when users need Alpha Vantage market data or indicators through the official Alpha Vantage API, including ticker lookup, time series retrieval, technical indicators, fundamentals, and deployment-safe API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscraters](https://clawhub.ai/user/oscraters)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to plan and implement Alpha Vantage API calls for market data, indicators, fundamentals, and related financial datasets. It helps agents choose endpoints, handle API keys, retry throttled requests, validate responses, and prepare public or commercial deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if hardcoded, logged, or passed directly on command lines.

Mitigation: Provide the key through ALPHAVANTAGE_API_KEY or a secret manager, avoid command-line key exposure, and mask keys in debug output.

Risk: Alpha Vantage rate limits or plan restrictions can interrupt workloads or affect public and commercial deployments.

Mitigation: Confirm the applicable Alpha Vantage plan and redistribution rights, pace multi-symbol jobs, and use bounded retries with backoff for throttled responses.

## Reference(s):

- [Alpha Vantage API Reference](artifact/references/api_docs.md)
- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code references, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint parameters, environment-variable setup, retry guidance, and normalized JSON response handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
