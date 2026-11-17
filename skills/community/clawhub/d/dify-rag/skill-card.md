## Description:

Dify.AI knowledge base read-only retrieval for shared use by other skills; it does not upload or modify content, which users manage in the Dify console.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahsh](https://clawhub.ai/user/mahsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw skills can retrieve relevant information from a shared Dify knowledge base for research and documentation tasks. If Dify is unavailable, they can fall back to local memory search and identify that source in their response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may contain sensitive information sent to the configured Dify service.

Mitigation: Use a Dify service you trust and avoid sending sensitive information in queries.

Risk: Runtime permissions are unknown, and the security review was partial because a referenced local path was missing.

Mitigation: Review the installed skill and its runtime permissions before use.

## Reference(s):

- [Dify knowledge API documentation](https://docs.dify.ai/zh/api-reference/guides/knowledge)
- [Dify RAG on ClawHub](https://clawhub.ai/mahsh/skills/dify-rag)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Formatted text or JSON retrieval results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to the requested number of matches (default 5); queries longer than 250 characters are truncated.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
