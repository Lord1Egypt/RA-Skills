## Description: <br>
Amazon Listing Audit Pro helps Amazon sellers audit listings across eight weighted dimensions, compare against category leaders, identify keyword gaps, and generate data-backed improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apiclaw](https://clawhub.ai/user/apiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers, agencies, and ecommerce operators use this skill to evaluate single or bulk ASIN listings, benchmark them against market leaders, and prioritize listing improvements. It is intended for external commercial workflows that use APIClaw data and require an APICLAW_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends ASINs, keywords, categories, competitor targets, and related business research to api.apiclaw.io. <br>
Mitigation: Install only if the user trusts APIClaw for this data, and avoid submitting confidential product strategy unless permitted by the user's data handling policy. <br>
Risk: The artifact includes code and reference material broader than the advertised listing-audit workflow. <br>
Mitigation: Invoke the listing-audit workflow for this skill unless the user intentionally requests broader APIClaw market-entry, opportunity, monitoring, pricing, or review-deepdive capabilities. <br>
Risk: Credential lookup supports APICLAW_API_KEY and local APIClaw configuration files. <br>
Mitigation: Prefer setting APICLAW_API_KEY explicitly for the session and review or remove local APIClaw config files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apiclaw/amazon-listing-audit-pro) <br>
- [APIClaw API documentation](https://api.apiclaw.io/api-docs) <br>
- [APIClaw API key setup](https://apiclaw.io/en/api-keys) <br>
- [APIClaw homepage](https://apiclaw.io) <br>
- [API field reference](references/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with scorecards, tables, recommendations, data provenance, and API usage details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report language should match the user's input language; conclusions are labeled as data-backed, inferred, or directional.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
