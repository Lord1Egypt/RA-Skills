## Description:

Goods Search helps agents handle shopping queries by using Viking AI Search chat or direct search APIs and formatting returned product results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyantong429-coder](https://clawhub.ai/user/chenyantong429-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to search for goods, retrieve candidate products, answer shopping questions, and generate product-card style recommendations from real service responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a plaintext API key.

Mitigation: Revoke the bundled key, remove it from distributed files, and require a user-controlled secret through environment configuration before use.

Risk: Shopping queries, optional images, user metadata, and location context can be sent to the configured Viking AI Search endpoint.

Mitigation: Use the skill only when that data flow is acceptable, avoid sensitive inputs, and disclose the external service dependency to users or operators.

Risk: The configured service endpoint is not independently validated by the artifact.

Mitigation: Restrict use to the documented HTTPS hosts and review endpoint configuration before deployment.

## Reference(s):

- [Search API reference](artifact/references/search_api.md)
- [ChatSearch API reference](artifact/references/chat_search_api.md)
- [Volcengine Search API documentation](https://www.volcengine.com/docs/85296/1544974?lang=zh)
- [Volcengine ChatSearch API documentation](https://www.volcengine.com/docs/85296/1873492?lang=zh)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [JSON service responses and concise Markdown product summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should use only fields returned by the search service; missing product fields are omitted rather than fabricated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
