## Description: <br>
Analyzes a public product image URL with Grok Vision AI and generates e-commerce product descriptions in professional, casual, luxury, or SEO styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, marketers, and developers use this skill to turn public product image URLs into listing-ready product descriptions. It supports English, Chinese, and Spanish output for Amazon, Shopify, and similar product-copy workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an x.ai API key. <br>
Mitigation: Provide XAI_API_KEY through a trusted environment or secret manager, and avoid exposing it in shell history, logs, or shared examples. <br>
Risk: Product image URLs are sent to api.x.ai for processing. <br>
Mitigation: Use only public, non-sensitive image URLs; avoid signed, private, internal, or sensitive links, and remove access-token or tracking query parameters before use. <br>
Risk: Vision-generated product copy can overstate or misread visible product features. <br>
Mitigation: Review generated descriptions before publishing, especially for regulated claims, pricing, safety, compatibility, or warranty language. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/ai-product-description-generator-from-image) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [x.ai API endpoint used by the skill](https://api.x.ai/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text product descriptions printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Description style can be professional, casual, luxury, or SEO; language can be English, Chinese, or Spanish.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
