## Description: <br>
Embed interactive flight price trend charts into AI responses. Requires SerpAPI key for real-time data. Use when users want to visualize 60-day price history for specific flight routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyikoi](https://clawhub.ai/user/keyikoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add interactive flight price history charts and buy-or-wait price analysis to AI responses after a route-specific flight search result is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real price history depends on SerpAPI configuration, and simulated or partial data can be mistaken for guaranteed market history. <br>
Mitigation: Clearly label simulated, partial, and real data in responses and avoid presenting chart output as guaranteed historical pricing. <br>
Risk: The artifact describes route-level price search snapshots being stored locally without retention or deletion controls. <br>
Mitigation: Add retention and deletion controls before using storage or scheduled-collection examples in production. <br>
Risk: SerpAPI keys are required for real-time data and could be exposed if placed in committed configuration files. <br>
Mitigation: Keep API keys out of committed files and use local or secret-managed configuration for credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keyikoi/flight-price-chart) <br>
- [Price Trend Technical References](references/README.md) <br>
- [Configure SerpAPI](references/configure-serpapi.md) <br>
- [Price Trend Data Sources](references/data-sources.md) <br>
- [Price Trend API Reference](references/price-api.md) <br>
- [Price Analysis Logic Reference](references/price-analysis.md) <br>
- [PriceChart Component Reference](references/price-chart-component.md) <br>
- [SerpAPI](https://serpapi.com/) <br>
- [SerpAPI Google Flights API](https://serpapi.com/google-flights-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with React or HTML component integration snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May render an embedded React or HTML price trend chart when supplied with route and price-history data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
