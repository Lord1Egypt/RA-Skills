## Description: <br>
Helps agents research Amazon product opportunities, competitors, pricing, reviews, risk, and listings using APIClaw data and guided analysis workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-srp](https://clawhub.ai/user/ryan-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, analysts, and developers use this skill to evaluate Amazon markets, discover product opportunities, inspect competitors, assess product risk, and prepare listing or pricing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be saved in plaintext configuration files. <br>
Mitigation: Prefer the APICLAW_API_KEY environment variable, avoid giving keys directly to the agent, avoid saving config.json, and rotate exposed keys. <br>
Risk: Seller nationality analysis can become unreliable if sellerLocation is unavailable. <br>
Mitigation: Use only verified sellerLocation data for seller-location claims and state that the data is unavailable when coverage is insufficient. <br>
Risk: The security verdict requires review before installation. <br>
Mitigation: Review the skill's credential handling and seller-location workflow before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryan-srp/apiclaw-analysis-skill) <br>
- [APIClaw OpenAPI specification](https://apiclaw.io/api/v1/openapi-spec) <br>
- [APIClaw API reference](references/reference.md) <br>
- [Composite and case-study scenarios](references/scenarios-composite.md) <br>
- [Evaluation and risk scenarios](references/scenarios-eval.md) <br>
- [Pricing scenarios](references/scenarios-pricing.md) <br>
- [Operations scenarios](references/scenarios-ops.md) <br>
- [Expansion scenarios](references/scenarios-expand.md) <br>
- [Listing scenarios](references/scenarios-listing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with tables, JSON-derived data summaries, and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API usage summaries, data-source notes, product comparisons, risk matrices, pricing guidance, listing recommendations, and credential setup guidance.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
