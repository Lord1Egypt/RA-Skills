## Description: <br>
Search Dify Knowledge Base (Dataset) to get accurate context for RAG-enhanced answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaowenzhou](https://clawhub.ai/user/xiaowenzhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to list and search Dify datasets for retrieval-augmented context in question answering, documentation search, and contextual responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries and API credentials to the Dify endpoint configured in DIFY_BASE_URL. <br>
Mitigation: Use a trusted Dify instance over HTTPS and configure a least-privileged DIFY_API_KEY. <br>
Risk: Search queries may include sensitive or regulated information. <br>
Mitigation: Avoid sending secrets or regulated data unless the configured Dify environment is approved for that data. <br>


## Reference(s): <br>
- [Dify Dataset API documentation](https://docs.dify.ai/reference/api-reference) <br>
- [ClawHub release page](https://clawhub.ai/xiaowenzhou/dify-kb-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIFY_API_KEY and DIFY_BASE_URL; returns dataset lists or search results with content, scores, titles, and document IDs.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
