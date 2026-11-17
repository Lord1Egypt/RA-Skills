## Description:

Fetch exchange rates and convert currencies with the free Frankfurter API (no API key). Use for any exchange rate, currency conversion, forex, or historical FX data task, even if Frankfurter isn't mentioned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve exchange rates, convert currencies, inspect historical foreign exchange data, and understand Frankfurter API endpoint behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exchange-rate requests to the public Frankfurter API can expose currency pairs, dates, and similar request parameters to that service.

Mitigation: Avoid including sensitive business context in requests unless the requester is comfortable sharing those parameters with the public API.

Risk: Frankfurter rates are daily reference rates rather than live market data, and the latest available date may be an earlier business day.

Mitigation: Read the returned date field and avoid using the data where live tick-level pricing is required.

Risk: Blended rates may shift as contributing provider data changes and may not be suitable for official or compliance workflows.

Mitigation: Use the providers parameter to pin an appropriate source when official provider-specific rates are required.

## Reference(s):

- [Frankfurter public API](https://api.frankfurter.dev)
- [Frankfurter API v2 endpoint reference](references/endpoints.md)
- [Frankfurter v1 API legacy reference](references/v1-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API examples, request patterns, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe JSON, CSV, or NDJSON response formats for Frankfurter API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
