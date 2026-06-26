## Description: <br>
Amazon product research and seller analytics for FBA and FBM businesses, including product selection, competitor tracking, BSR monitoring, review analysis, sales estimation, listing optimization, and market opportunity assessment via APIClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christine-srp](https://clawhub.ai/user/christine-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, FBA and FBM operators, and ecommerce analysts use this skill to query APIClaw for product discovery, competitor analysis, risk assessment, pricing strategy, market monitoring, and listing optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Amazon research queries to the external APIClaw service and consumes APIClaw quota. <br>
Mitigation: Use a dedicated APICLAW_API_KEY, confirm bulk lookups before execution, and make API usage visible in final analysis. <br>
Risk: Credential guidance is inconsistent because artifact behavior supports both environment variables and config.json fallback storage. <br>
Mitigation: Prefer APICLAW_API_KEY in the environment and avoid asking an agent to save API keys to disk. <br>
Risk: Seller-location analysis can become unsafe when it infers Chinese seller status from brand or seller-name patterns instead of explicit sellerLocation data. <br>
Mitigation: Use only explicit sellerLocation data for location-based seller analysis and disclose missing or low-coverage location data. <br>


## Reference(s): <br>
- [APIClaw API Reference](references/reference.md) <br>
- [Amazon Seller Comprehensive Analysis & Case Studies](references/scenarios-composite.md) <br>
- [Amazon Product Evaluation & Risk Assessment](references/scenarios-eval.md) <br>
- [Amazon Pricing Strategy & Profit Estimation](references/scenarios-pricing.md) <br>
- [Amazon Seller Daily Operations & Monitoring](references/scenarios-ops.md) <br>
- [Amazon Product Expansion & Market Trends](references/scenarios-expand.md) <br>
- [Amazon Listing Optimization & Content Creation](references/scenarios-listing.md) <br>
- [APIClaw](https://apiclaw.io) <br>
- [APIClaw API Keys](https://apiclaw.io/api-keys) <br>
- [APIClaw OpenAPI Spec](https://apiclaw.io/api/v1/openapi-spec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with API-derived tables, concise recommendations, command examples, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY and may consume APIClaw quota when the agent executes API-backed workflows.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact frontmatter says 1.1.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
