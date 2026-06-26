## Description: <br>
Finds Amazon product opportunities with preset selection strategies, market research, competitor lookup, risk assessment, pricing support, review analysis, and listing optimization using the APIClaw API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-srp](https://clawhub.ai/user/ryan-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and agents use this skill to research product opportunities, analyze competitors, assess market and listing risks, estimate pricing, and generate seller-facing recommendations from APIClaw data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be stored in plaintext when the config.json fallback is used. <br>
Mitigation: Prefer APICLAW_API_KEY as an environment variable and avoid giving the key to the agent for file-based storage. <br>
Risk: The Chinese seller workflow relies on weak nationality proxies and may produce biased or discriminatory analysis. <br>
Mitigation: Avoid that workflow unless it has been reviewed for the intended use case, and treat any nationality-based conclusions as unsuitable for automated decisions. <br>
Risk: The skill sends product research requests to the APIClaw service. <br>
Mitigation: Install and use it only when APIClaw is an approved data provider for the user's Amazon seller research workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryan-srp/amazon-analysis-skill) <br>
- [APIClaw](https://apiclaw.io) <br>
- [APIClaw API keys](https://apiclaw.io/api-keys) <br>
- [APIClaw OpenAPI spec](https://apiclaw.io/api/v1/openapi-spec) <br>
- [API reference](references/reference.md) <br>
- [Composite scenarios](references/scenarios-composite.md) <br>
- [Evaluation scenarios](references/scenarios-eval.md) <br>
- [Pricing scenarios](references/scenarios-pricing.md) <br>
- [Operations scenarios](references/scenarios-ops.md) <br>
- [Expansion scenarios](references/scenarios-expand.md) <br>
- [Listing scenarios](references/scenarios-listing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON command outputs and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY and may include API usage summaries for generated analyses.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
