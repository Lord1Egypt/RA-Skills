## Description:

Search pre-indexed developer documentation across 10 platforms including Cloudflare, Stripe, Anthropic, OpenAI, Next.js, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to look up supported API and framework documentation, retrieve source-linked documentation chunks, and ground implementation guidance for indexed platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation lookup queries are sent to an external service.

Mitigation: Avoid sending secrets, proprietary code, credentials, or sensitive user data in lookup queries.

Risk: Some query and lookup endpoints are described as paid x402 operations.

Mitigation: Approve paid x402 use deliberately before making paid requests.

Risk: The skill only covers its indexed platform list.

Mitigation: Use returned source URLs and relevance scores, and fall back gracefully when a platform or topic is not indexed.

## Reference(s):

- [Docs Lookup ClawHub page](https://clawhub.ai/cutthemustard/skills/docs-lookup)
- [AgentUtil documentation lookup service](https://docs.agentutil.net)
- [AgentUtil indexed platforms endpoint](https://docs.agentutil.net/platforms)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with source URLs and optional JSON or bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include relevance scores, request identifiers, and source documentation URLs returned by lookup results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
