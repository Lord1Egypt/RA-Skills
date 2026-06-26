## Description: <br>
Amazon product research and seller analytics for FBA and FBM businesses, including product selection, ASIN lookup, BSR analysis, competitor tracking, review analysis, pricing strategy, listing optimization, and market opportunity assessment using APIClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christine-srp](https://clawhub.ai/user/christine-srp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon FBA and FBM sellers, ecommerce operators, and their AI agents use this skill to research product opportunities, compare competitors, assess risks, estimate sales, analyze reviews, and draft or optimize listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys could be exposed if pasted into chat or stored in local configuration without controlled file permissions. <br>
Mitigation: Use the APICLAW_API_KEY environment variable, avoid sharing secrets in chat, and only use config.json when local file permissions are controlled. <br>
Risk: Seller-origin workflows could produce nationality-based profiling or unsupported inferences. <br>
Mitigation: Limit seller-origin analysis to verified sellerLocation fields and avoid inferring nationality from names, brands, categories, or stereotypes. <br>
Risk: Broad activation guidance or bulk workflows could trigger unnecessary external API calls. <br>
Mitigation: Run API calls only for clear Amazon seller-research tasks and confirm with the user before bulk ASIN lookups. <br>
Risk: Snapshot or delayed data could be mistaken for historical trends or current live values. <br>
Mitigation: Disclose API source, date range, filters, and known data freshness limits; use realtime/product for current price, BSR, and rating fields where available. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/christine-srp/amazon-seller-research) <br>
- [APIClaw API reference](references/reference.md) <br>
- [Amazon seller comprehensive analysis and case studies](references/scenarios-composite.md) <br>
- [Amazon product evaluation and risk assessment](references/scenarios-eval.md) <br>
- [Amazon listing optimization and content creation](references/scenarios-listing.md) <br>
- [Amazon seller daily operations and monitoring](references/scenarios-ops.md) <br>
- [Amazon product expansion and market trends](references/scenarios-expand.md) <br>
- [Amazon pricing strategy and profit estimation](references/scenarios-pricing.md) <br>
- [APIClaw OpenAPI spec](https://apiclaw.io/api/v1/openapi-spec) <br>
- [APIClaw API key setup](https://apiclaw.io/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown responses with tables, inline shell commands, and JSON from API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APICLAW_API_KEY; Full-mode analyses include data-source conditions and API usage summaries.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
