## Description: <br>
Queries Amazon product details by ASIN or product URL through the Clawec API and helps summarize item-level product research details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ecommerce operators use this skill to query Amazon product details from a product URL or ASIN plus region, then summarize returned fields for product research, competitor analysis, and item review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Clawec API key and sends Amazon product URLs or ASINs to Clawec. <br>
Mitigation: Keep the API key in the CLAWEC_API_KEY environment variable, avoid hardcoding credentials, and use the skill only when sending product research data to Clawec is acceptable. <br>
Risk: Returned product fields are dynamic and may vary by item, site region, or API response. <br>
Mitigation: Parse the data object defensively, show fields that are actually returned, and label unknown fields clearly in user-facing summaries. <br>


## Reference(s): <br>
- [Response schema](references/response-schema.md) <br>
- [Clawec Amazon ASIN query API endpoint](https://www.clawec.com/api/aigc/tool/amazon_asin_query) <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-amazon-asin-query) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses actual API response fields dynamically; common summaries include title, price, rating, reviews, sales, category, brand, images, and links when returned.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
