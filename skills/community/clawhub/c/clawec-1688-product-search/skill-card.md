## Description: <br>
通过 Clawec API 搜索 1688 商品，返回价格、销量、链接、卖家信息与 AI 建议。在用户需要 1688 搜品、货源调研、供应链比价、跨境选品、关键词找货、1688 产品搜索时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anyunzhong](https://clawhub.ai/user/anyunzhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cross-border ecommerce sellers, sourcing researchers, and agents use this skill to search 1688 product listings through the ClawEC API and summarize price, sales, seller, link, and AI-suggested sourcing information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ClawEC API key and sends product search keywords or sourcing research terms to ClawEC. <br>
Mitigation: Use a scoped API key where possible, keep the key in CLAWEC_API_KEY rather than hardcoding it, and avoid sending sensitive business research terms unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [Response Schema](references/response-schema.md) <br>
- [ClawEC API](https://www.clawec.com/api) <br>
- [ClawEC API Key](https://www.clawec.com/api-key?source=q-clawhub) <br>
- [ClawHub Skill Page](https://clawhub.ai/anyunzhong/clawec-1688-product-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with tables and optional shell commands; raw API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the CLAWEC_API_KEY environment variable and sends search keywords, page, and table parameters to the ClawEC API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
