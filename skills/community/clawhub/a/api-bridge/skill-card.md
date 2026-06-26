## Description: <br>
Curated free public APIs for AI agents - geocoding, weather, forex, validation, facts, finance, and test data. Use when an agent needs real-world data without paid API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexuser](https://clawhub.ai/user/alexuser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this documentation-first skill to choose public API endpoints and compose HTTP requests for weather, geocoding, exchange rates, validation, reference, finance, and test data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the example endpoints can send lookup data to third-party public API providers. <br>
Mitigation: Avoid sending confidential addresses, internal URLs, private IPs, sensitive domains, or business-sensitive finance queries unless sharing that data with those providers is acceptable. <br>
Risk: Some listed public APIs have rate limits, uptime variance, CORS constraints, or require request headers such as a User-Agent. <br>
Mitigation: Follow the skill's reliability notes, cache responses where appropriate, respect provider limits, and review service terms before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexuser/api-bridge) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [Nominatim Search API](https://nominatim.openstreetmap.org/search) <br>
- [ExchangeRate API latest rates](https://open.er-api.com/v6/latest/USD) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>
- [Wikipedia REST API](https://en.wikipedia.org/api/rest_v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with endpoint patterns and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; agents invoke third-party public APIs directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
