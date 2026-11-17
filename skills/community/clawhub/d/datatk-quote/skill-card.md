## Description:

Real-time stock market data via QuoteNode API. Query quotes, K-lines, tick trades, Level-2 depth, and trading calendars for US/HK/CN markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengxiaozi-liu](https://clawhub.ai/user/fengxiaozi-liu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and call QuoteNode/dataTrack REST market-data endpoints for quotes, historical bars, tick trades, Level-2 depth, instrument lists, broker data, and trading calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and request bodies are sent to the configured QuoteNode/dataTrack service.

Mitigation: Keep env.json private, use a trusted datatk HTTPS endpoint, and avoid placing unrelated sensitive data in request bodies.

## Reference(s):

- [QuoteNode REST Architecture Summary](references/architecture.md)
- [QuoteNode REST API Guide](references/openapi.md)
- [QuoteNode Enums and Error Codes](references/reference.md)
- [QuoteNode REST Response Field Guide](references/response.md)
- [dataTrack service page](https://www.datatk.com/service)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and raw JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an env.json file with endpoint and API key; the request script posts JSON bodies to allowlisted datatk HTTPS endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
