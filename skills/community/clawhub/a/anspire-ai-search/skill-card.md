## Description:

Anspire Search lets agents perform real-time web search through Anspire's API using a Python or shell wrapper and an ANSPIRE_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anspire-ai](https://clawhub.ai/user/anspire-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve current web results, news, market updates, research references, and other time-sensitive facts inside an OpenClaw agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and result requests are sent to Anspire's search API.

Mitigation: Use the skill only for queries you are comfortable sharing with Anspire, and avoid submitting sensitive personal, customer, or confidential business data.

Risk: The skill documentation encourages collecting and persisting ANSPIRE_API_KEY values in shell startup files.

Mitigation: Have users set credentials themselves through a secret manager or temporary environment variable, and review any proposed shell startup file changes before applying them.

Risk: The skill strongly steers web searches to a single provider.

Mitigation: Treat returned results as provider-specific search output and corroborate important claims with cited sources or another trusted source when accuracy matters.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/anspire-ai/skills/anspire-ai-search)
- [Anspire Search](https://aisearch.anspire.cn)
- [Anspire Search API endpoint](https://plugin.anspire.cn/api/ntsearch/search)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include title, URL, content, score, and publication date fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
