## Description:

AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily-powered web searches, retrieve concise source-backed results, and extract readable content from supplied URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, requested URLs, and the Tavily API key are sent to Tavily's API when the skill is invoked.

Mitigation: Use the skill only when that data sharing is acceptable, manage TAVILY_API_KEY as a secret, and avoid submitting sensitive queries or URLs.

Risk: Search and extraction results depend on Tavily API responses and may be incomplete or unsuitable for high-stakes decisions without review.

Mitigation: Review returned sources and extracted content before relying on the output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/williamwang-wh/skills/claw-tavily-search-pro)
- [Publisher Profile](https://clawhub.ai/user/williamwang-wh)
- [Tavily Homepage](https://tavily.com)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown sections containing answers, sources, extracted content, and failed URL reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is clamped to 1-20 and output depends on Tavily API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
