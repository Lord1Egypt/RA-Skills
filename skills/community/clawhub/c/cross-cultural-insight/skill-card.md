## Description: <br>
Provides cultural risk analysis for brand names, color symbolism, and market entry strategies across 50+ regions to support global brand compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brand, localization, and market-entry teams use this skill to check names, colors, symbols, and regional market assumptions before launching in new markets. Agents can call the disclosed API with brand and target-market parameters to return cultural guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an unencrypted HTTP endpoint, so submitted brand names, product categories, and market-entry context could be observed or modified in transit. <br>
Mitigation: Avoid sending confidential launch plans, sensitive client data, or unreleased brand strategy unless the publisher and transport risk are acceptable. <br>
Risk: The skill is a third-party API-based branding tool, so users rely on the publisher-operated service for generated cultural guidance. <br>
Mitigation: Review the guidance with qualified localization, legal, or regional experts before making launch or compliance decisions. <br>


## Reference(s): <br>
- [Cross-Cultural Insight ClawHub listing](https://clawhub.ai/ai-gaoqian/cross-cultural-insight) <br>
- [Cross-Cultural Insight reference metadata](references/cross-cultural-insight.json) <br>
- [Cross-Cultural Insight API endpoint](http://8.145.54.67:3000/skill/cross-cultural-insight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API responses] <br>
**Output Format:** [Text or JSON-style API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may depend on brand_name, target_market, and product_type query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
