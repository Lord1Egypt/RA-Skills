## Description:

Embed interactive flight price trend charts into AI responses. Requires SerpAPI key for real-time data. Use when users want to visualize 60-day price history for specific flight routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyikoi](https://clawhub.ai/user/keyikoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add flight price trend charts and buy/wait guidance to AI or agent flight-search responses with confirmed origin-destination pairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe browser rendering patterns can expose users to injected content when AI output or untrusted data is rendered as HTML.

Mitigation: Use the React chart component with validated structured data, avoid the raw HTML rendering examples unless sanitization is added, and do not render AI output through innerHTML or dangerouslySetInnerHTML.

Risk: API keys may be exposed if SerpAPI or related credentials are stored in committed JSON configuration files.

Mitigation: Store API keys outside committed files, use environment or secret-management configuration, and review configuration before release.

Risk: Stored flight-search and price-history data can create privacy or retention obligations.

Mitigation: Enable price-history storage or scheduled collection only after defining retention, access, and privacy controls.

Risk: Simulated or partial flight-price history can make buy/wait guidance sound more certain than the data supports.

Mitigation: Label estimated, partial, and real data clearly, include confidence wording, and avoid strong purchase recommendations when route history is insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyikoi/skills/flight-price-chart)
- [SerpAPI configuration guide](references/configure-serpapi.md)
- [PriceChart component reference](references/price-chart-component.md)
- [Price trend API reference](references/price-api.md)
- [Price analysis logic reference](references/price-analysis.md)
- [Data sources reference](references/data-sources.md)
- [SerpAPI documentation](https://serpapi.com/)
- [SerpAPI Google Flights API](https://serpapi.com/google-flights-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSX, HTML, JavaScript, and JSON data examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to append an interactive price chart and concise buy/wait recommendation; real-time price data requires a SerpAPI key, and simulated or partial data should be disclosed.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
