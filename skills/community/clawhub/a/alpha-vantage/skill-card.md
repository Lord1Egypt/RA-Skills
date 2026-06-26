## Description: <br>
Use this skill when users need Alpha Vantage market data or indicators via the official API, including ticker lookups, time series pulls, technical indicators, fundamentals, API integration code, and deployment-safe workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build Alpha Vantage API requests, retrieve and normalize market data, handle throttling and errors, and prepare API integrations for public or commercial deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys could be exposed if passed directly in prompts, command history, logs, or source files. <br>
Mitigation: Use the ALPHAVANTAGE_API_KEY environment variable or a secret manager, and mask keys in debug output. <br>
Risk: Repeated agent requests can exhaust Alpha Vantage quota or trigger throttling. <br>
Mitigation: Use bounded retries with backoff, cache stable responses, pace multi-symbol jobs to the active plan, and monitor throttle rates. <br>
Risk: Market data responses can contain API errors, empty payloads, string-encoded numbers, or function-specific schemas. <br>
Mitigation: Validate transport and payload success, handle Error Message and Note responses, preserve metadata, and normalize results before downstream use. <br>
Risk: Public or commercial deployments may exceed the usage rights or capacity of the selected Alpha Vantage plan. <br>
Mitigation: Review Alpha Vantage terms and plan limits before release, and avoid redistributing restricted content when terms disallow it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oscraters/alpha-vantage) <br>
- [Alpha Vantage API Reference](references/api_docs.md) <br>
- [Alpha Vantage Documentation](https://www.alphavantage.co/documentation/) <br>
- [Alpha Vantage API Key](https://www.alphavantage.co/support/#api-key) <br>
- [Alpha Vantage Premium Plans](https://www.alphavantage.co/premium/) <br>
- [Alpha Vantage Terms of Service](https://www.alphavantage.co/terms_of_service/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and optional Python helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment-variable based API key handling, bounded retries, throttling detection, and response validation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
