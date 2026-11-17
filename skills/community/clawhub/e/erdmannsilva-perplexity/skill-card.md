## Description:

Search the web with AI-powered answers via Perplexity API. Returns grounded responses with citations. Supports batch queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erdmannsilva](https://clawhub.ai/user/erdmannsilva)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run single or batch Perplexity web searches from an agent workflow and receive grounded results with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Perplexity using the user's API key.

Mitigation: Do not include private credentials, confidential documents, or sensitive personal data in queries unless that sharing is intended.

## Reference(s):

- [Perplexity API Documentation](https://docs.perplexity.ai)
- [Perplexity Search API Endpoint](https://api.perplexity.ai/search)
- [ClawHub Skill Page](https://clawhub.ai/erdmannsilva/skills/erdmannsilva-perplexity)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown-formatted search results or raw JSON when --json is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and PERPLEXITY_API_KEY; sends user-provided queries to Perplexity.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
