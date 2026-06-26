## Description: <br>
Searches real product data for prices, availability, merchant links, product recommendations, comparisons, and visual-similarity shopping queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanfen-c3](https://clawhub.ai/user/evanfen-c3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to find products, compare prices, check merchant availability, and produce concise recommendations from Channel3 catalog results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries and image URLs are sent to Channel3. <br>
Mitigation: Avoid sensitive personal information in searches and only install when that data sharing is acceptable. <br>
Risk: The skill uses a Channel3 API key and may consume credits or incur billing. <br>
Mitigation: Use a dedicated API key and monitor credit or billing usage. <br>
Risk: Product buy links redirect through buy.trychannel3.com with affiliate tracking. <br>
Mitigation: Disclose redirected merchant links when presenting results and let users inspect links before purchase. <br>


## Reference(s): <br>
- [Skill listing](https://clawhub.ai/evanfen-c3/channel3-product-discovery) <br>
- [Channel3](https://trychannel3.com) <br>
- [Channel3 API docs](https://docs.trychannel3.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries based on structured text product search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, network access to api.trychannel3.com, and a CHANNEL3_API_KEY secret.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
