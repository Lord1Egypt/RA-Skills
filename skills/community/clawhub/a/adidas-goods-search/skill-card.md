## Description: <br>
Routes shopping-related queries to Volcengine Viking AI Search chat or search APIs and formats real returned product fields into product lists, product cards, or conversational answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyantong429-coder](https://clawhub.ai/user/chenyantong429-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to decide between conversational shopping search and direct product retrieval, then present returned product data as concise recommendations, lists, or cards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact bundles and automatically uses an external API key. <br>
Mitigation: Remove or rotate the bundled key before installation and require a user-provided, scoped credential. <br>
Risk: Shopping queries, image inputs, optional user fields, and optional location context may be sent to Volcengine AI Search. <br>
Mitigation: Review data-sharing requirements before use and avoid sending sensitive user, image, or location data unless authorized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenyantong429-coder/adidas-goods-search) <br>
- [ChatSearch API reference](artifact/references/chat_search_api.md) <br>
- [Search API reference](artifact/references/search_api.md) <br>
- [Volcengine ChatSearch documentation](https://www.volcengine.com/docs/85296/1873492?lang=zh) <br>
- [Volcengine Search documentation](https://www.volcengine.com/docs/85296/1544974?lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown product summaries and structured JSON search or chat responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses only fields returned by the search service and omits missing product details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
