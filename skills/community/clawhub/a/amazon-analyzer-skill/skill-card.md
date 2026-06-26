## Description: <br>
APIClaw Amazon Analysis helps agents perform Amazon product research, market validation, competitor analysis, pricing, review analysis, listing optimization, and risk assessment using the APIClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyle-srp](https://clawhub.ai/user/kyle-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, ecommerce analysts, and agent developers use this skill to research products, categories, competitors, pricing, reviews, listings, and operational signals for Amazon selling decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist API keys in plaintext config.json when users provide a key through the agent. <br>
Mitigation: Prefer APICLAW_API_KEY as an environment variable, avoid pasting keys into chat, and remove any local config.json when it is no longer needed. <br>
Risk: Amazon seller research queries are sent to the third-party APIClaw service. <br>
Mitigation: Install only when this data sharing is acceptable and avoid including confidential business details that are not needed for the query. <br>
Risk: The Chinese seller case-study workflow can encourage nationality-based profiling. <br>
Mitigation: Avoid or tightly constrain that workflow, use neutral business metrics, and clearly disclose data coverage limits when seller-location fields are missing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kyle-srp/amazon-analyzer-skill) <br>
- [APIClaw API reference](references/reference.md) <br>
- [APIClaw OpenAPI specification](https://apiclaw.io/api/v1/openapi-spec) <br>
- [Product evaluation scenarios](references/scenarios-eval.md) <br>
- [Composite recommendation scenarios](references/scenarios-composite.md) <br>
- [Pricing scenarios](references/scenarios-pricing.md) <br>
- [Listing scenarios](references/scenarios-listing.md) <br>
- [Operations scenarios](references/scenarios-ops.md) <br>
- [Expansion scenarios](references/scenarios-expand.md) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with inline shell commands and JSON API outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY; API responses are used as evidence for market and product guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
