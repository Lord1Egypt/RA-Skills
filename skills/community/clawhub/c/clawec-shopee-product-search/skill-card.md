## Description: <br>
Searches Shopee products through the ClawEC API and returns product prices, sales, ratings, markets, links, and images for product research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce operators use this skill to search Shopee listings and compare products for Southeast Asia cross-border ecommerce product research, competitive analysis, and keyword-based sourcing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Shopee search keywords, region values, and the ClawEC API key to clawec.com. <br>
Mitigation: Keep the API key in CLAWEC_API_KEY and avoid using sensitive private business terms unless that sharing is intended. <br>


## Reference(s): <br>
- [Response Schema](references/response-schema.md) <br>
- [ClawEC API Base URL](https://www.clawec.com/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/clawec-shopee-product-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summaries and tables with JSON API responses when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Product results may include names, prices, sales, ratings, rankings, markets, links, image URLs, and API point information.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
