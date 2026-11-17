## Description:

Federated web search across 10+ search engines (DuckDuckGo, Brave, Google, Bing), multi-language, news-aware, answer-first results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run federated web and news searches, produce answer-first results with sources, and monitor topics for newly discovered links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The core runtime is incomplete, so search and cache behavior cannot be fully reviewed from the supplied artifact.

Mitigation: Review the missing runtime files and cache behavior before installation or use with sensitive workflows.

Risk: The monitor can write state files outside its intended temporary folder when untrusted tag values are used.

Mitigation: Use fixed simple tag values containing only letters, numbers, underscores, or hyphens.

Risk: Search queries and provider credentials may be sensitive.

Mitigation: Avoid sensitive queries and provider API keys until the supplied files and security guidance have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/clawsearch-ultra)
- [Publisher profile](https://clawhub.ai/user/northcap-group)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON search results with source URLs and provider/routing metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit cached search telemetry, provider selection, routing summaries, and watch-state updates.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
