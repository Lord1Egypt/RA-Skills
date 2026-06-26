## Description: <br>
Searches Temu products through the Clawec API and returns product details such as price, sales, rating, market, links, and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and agents use this skill to search Temu products for product sourcing, competitor research, keyword-based discovery, and market comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Clawec API key, which could be exposed if pasted into chats, scripts, or logs. <br>
Mitigation: Store CLAWEC_API_KEY in an environment variable and avoid hardcoding or sharing the key. <br>
Risk: Search keywords are sent to Clawec as part of the product-search request. <br>
Mitigation: Use the skill only when sending those search terms to Clawec is acceptable for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anyunzhong/clawec-temu-product-search) <br>
- [Temu product search response schema](references/response-schema.md) <br>
- [Clawec API base URL](https://www.clawec.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and tables, with optional shell command examples and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include product names, prices, sales, ratings, ranking, market, links, image URLs, and Clawec point information when returned by the API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
