## Description: <br>
Provides 1688 product discovery through official 1688 Open Platform APIs, including category lookup, keyword and image search, product detail lookup, shop search, recommendations, and product pool pulls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688AiInfra](https://clawhub.ai/user/1688AiInfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and sourcing agents use this skill to search 1688 listings by keyword, image, seller, category, or product ID and return product IDs, product links, pricing, sales, seller, and recommendation data for procurement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires 1688 API credentials and can cache reusable account tokens in a shared local token file. <br>
Mitigation: Install only where 1688 account access is appropriate, protect the credential environment variables, and restrict or periodically clear the shared .1688_token_cache.json file. <br>
Risk: Image search can send selected product images or image URLs to 1688 and may fetch user-supplied image URLs. <br>
Mitigation: Use only public product images or trusted image URLs; avoid private screenshots, sensitive documents, internal URLs, localhost URLs, and cloud-metadata URLs. <br>
Risk: The security verdict is suspicious because the skill combines token storage with image upload and URL-fetching behavior. <br>
Mitigation: Review the skill before deployment and limit use to workflows where these credential and image-handling behaviors are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688AiInfra/1688-product-search) <br>
- [1688 Product Search API reference](references/api.md) <br>
- [1688 Open Platform](https://open.1688.com) <br>
- [1688 API invocation guide](https://open.1688.com/doc/apiInvoke.htm) <br>
- [1688 signature rules](https://open.1688.com/doc/signature.htm) <br>
- [1688 authorization guide](https://open.1688.com/doc/apiAuth.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [JSON API responses and Markdown-ready product summaries with product IDs and links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires 1688 API credentials through ALI1688_APP_KEY, ALI1688_APP_SECRET, and ALI1688_REFRESH_TOKEN; image search may send selected image URLs or uploaded images to 1688 APIs.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
