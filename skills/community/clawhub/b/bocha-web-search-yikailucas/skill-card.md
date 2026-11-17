## Description:

Bocha Web Search wraps Bocha Web Search, AI Search, Agent Search, and Semantic Reranker APIs with Node.js and shell entrypoints that accept standard parameters or raw JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to run Bocha-powered Chinese web search, answer augmentation, source-oriented retrieval, and reranking workflows from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, raw JSON fields, and reranker documents are sent to Bocha as a third-party provider.

Mitigation: Do not include private or sensitive content unless that provider use is acceptable for the deployment.

Risk: Generic web-search prompts could trigger this third-party API when the agent has multiple search tools available.

Mitigation: Confirm tool choice for broad web-search requests and prefer explicit Bocha requests where provider selection matters.

Risk: The skill requires a Bocha API key.

Mitigation: Use the BOCHA_API_KEY environment variable where possible and avoid committing local config.json files with secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yikailucas/skills/bocha-web-search-yikailucas)
- [Bocha Web Search API endpoint](https://api.bochaai.com/v1/web-search)
- [Bocha AI Search API endpoint](https://api.bochaai.com/v1/ai-search)
- [Bocha Agent Search API endpoint](https://api.bochaai.com/v1/agent-search)
- [Bocha Semantic Reranker API endpoint](https://api.bochaai.com/v1/semantic-reranker)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [JSON API responses with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bocha API key; result count is clamped to 1-50 and requests use a configurable timeout.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
