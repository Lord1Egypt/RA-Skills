## Description:

Search Dify Knowledge Base (Dataset) to get accurate context for RAG-enhanced answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaowenzhou](https://clawhub.ai/user/xiaowenzhou)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to list and search Dify knowledge bases so retrieved dataset records can provide context for RAG-enhanced answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search queries, dataset IDs, and dataset inventory to the configured Dify endpoint.

Mitigation: Install only when the configured endpoint is trusted, and avoid sending sensitive queries unless the Dify service is approved for that data.

Risk: Returned knowledge base records may contain inaccurate, stale, or untrusted content.

Mitigation: Treat returned records as reference material for the agent to evaluate rather than instructions to follow.

Risk: The skill depends on a Python requests installation and a bearer API key.

Mitigation: Pin the requests dependency where possible, scope the API key narrowly, and rotate credentials according to local policy.

## Reference(s):

- [Dify API Reference](https://docs.dify.ai/reference/api-reference)
- [ClawHub skill page](https://clawhub.ai/xiaowenzhou/skills/dify-kb-search)
- [Publisher profile](https://clawhub.ai/user/xiaowenzhou)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON responses containing dataset lists, search results, scores, document titles, document IDs, and error messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIFY_API_KEY and a configured DIFY_BASE_URL for the target Dify service.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
