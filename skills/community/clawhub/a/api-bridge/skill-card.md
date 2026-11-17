## Description:

Curated free public APIs for AI agents covering geocoding, weather, forex, validation, facts, finance, and test data when real-world data is needed without paid API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexuser](https://clawhub.ai/user/alexuser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to select public API endpoints for weather, geocoding, exchange rates, crypto prices, validation, facts, reference lookups, finance data, and test data. It provides endpoint patterns, expected output shapes, and curl examples for mostly key-free APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send API query parameters to public third-party services.

Mitigation: Avoid secrets and sensitive personal data, prefer HTTPS URLs, and get user approval before looking up IP addresses, precise locations, private URLs, or account-related finance data.

Risk: Some referenced APIs are rate limited, require a User-Agent, or are identified by the artifact as less reliable.

Mitigation: Cache responses where appropriate, respect service rate limits and User-Agent requirements, and prefer the artifact's reliable APIs for production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexuser/skills/api-bridge)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [ipapi IP Geolocation API](https://ipapi.co/json/)
- [Nominatim Search API](https://nominatim.openstreetmap.org/search)
- [ExchangeRate-API Open Rates](https://open.er-api.com/v6/latest/USD)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [icon.horse Favicon API](https://icon.horse/)
- [urlmeta Metadata API](https://urlmeta.org/?url=https://example.com)
- [Wikipedia REST API](https://en.wikipedia.org/api/rest_v1)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com)
- [Random User API](https://randomuser.me/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint patterns, JSON output descriptions, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agents may use the guidance to make HTTPS requests to public third-party APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
