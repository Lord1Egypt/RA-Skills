## Description:

Searches Google Finance for stocks, indices, funds, currencies, or futures through the Dataify Scraper API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to translate finance lookup requests into Dataify Google Finance searches and return stock, index, fund, currency, or futures data. It is not intended for general web search or personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance search parameters are sent to Dataify's scraper API.

Mitigation: Review request parameters before execution when they contain sensitive or ambiguous information, and use the skill only for finance lookups.

Risk: Passing a Dataify token on the command line can expose it through shell history or process inspection.

Mitigation: Set DATAIFY_API_TOKEN through the shell environment or a secret manager, and never paste the token into chat.

Risk: Successful uncached calls may consume Dataify account credits.

Mitigation: Use documented defaults unless the user requests cache bypass, and monitor Dataify credit usage.

Risk: Returned finance data may be incomplete, delayed, or unsuitable for personalized financial advice.

Mitigation: Preserve source links, distinguish missing fields from empty values, and avoid presenting results as personalized investment guidance.

## Reference(s):

- [Dataify Google Finance API](references/google_finance_api.md)
- [Dataify Google Finance release page](https://clawhub.ai/dataify-server/skills/dataify-google-finance)
- [Dataify publisher profile](https://clawhub.ai/user/dataify-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries by default, with raw JSON or HTML when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Dataify API token. The finance query q is required; documented defaults include json=1, window=1D, and no_cache=false.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
