## Description:

AI-optimized web search via AIsa's Tavily API proxy. Returns concise, relevant results for AI agents through AIsa's unified API gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run concise web searches, retrieve source snippets, and extract public URL content through AIsa/Tavily from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, requested URLs, and the AISA_API_KEY bearer token are sent to api.aisa.one.

Mitigation: Use the skill only when that disclosure is acceptable, avoid private or secret-bearing URLs, and manage the API key with normal credential hygiene.

Risk: URL extraction can disclose the target URL and retrieved content to AIsa/Tavily.

Mitigation: Run extraction only for public or approved URLs and avoid internal, private, or sensitive resources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/skills/ai-native-websearch-via-tavily-api-returns-concise-relevant-results-for-openclaw)
- [AIsa](https://aisa.one)
- [AIsa Marketplace](https://marketplace.aisa.one)
- [AIsa Tavily Search Endpoint](https://api.aisa.one/apis/v1/tavily/search)
- [AIsa Tavily Extract Endpoint](https://api.aisa.one/apis/v1/tavily/extract)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted command output with answer text, source listings, extracted content, and failed URL notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is clamped from 1 to 20; news searches can be limited by recent days; extraction accepts one or more URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
