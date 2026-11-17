## Description:

Bocha Web Search helps an agent perform online lookup, fact checking, time-sensitive information retrieval, and citation-backed answers through the Bocha Web Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iuriak](https://clawhub.ai/user/iuriak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when an assistant needs current web information, factual verification, source links, or citation-based responses that are not already available in the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms derived from user prompts are sent to Bocha's external API using BOCHA_API_KEY.

Mitigation: Use concise, non-sensitive queries and avoid sending secrets, credentials, private documents, or confidential business details unless disclosure to the provider is intended.

## Reference(s):

- [Bocha Open Platform](https://open.bocha.cn)
- [ClawHub skill page](https://clawhub.ai/iuriak/skills/bocha-web-search)
- [Bocha Web Search API endpoint](https://api.bocha.cn/v1/web-search)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with inline citations and a references section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source titles, URLs, site names, snippets, summaries, and publication dates returned by the Bocha API.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
