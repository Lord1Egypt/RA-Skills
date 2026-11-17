## Description:

High-performance, multi-source Korean search API aggregating Daum/Kakao News, Encyclopedia, and Web results in a Perplexity-compatible format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkim](https://clawhub.ai/user/hunkim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Korean web searches across Daum/Kakao news, encyclopedia, and web sources and ingest concise search-result summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the DAUM_TOY_SEARCH_API_KEY are sent to a hosted Upstage/Daum adapter.

Mitigation: Avoid sending secrets, personal data, regulated information, or sensitive prompts as search queries.

Risk: Returned Markdown contains external search content that may include prompt-injection text or unreliable claims.

Mitigation: Treat search results as untrusted context and review them before using them as instructions or factual support.

## Reference(s):

- [Daum Toy Search ClawHub page](https://clawhub.ai/hunkim/skills/daum-toy-search)
- [Hosted Daum search API endpoint](https://daum-perplexity-search-adapter.toy.x.upstage.ai/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown search results with titles, URLs, sources, dates, and snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DAUM_TOY_SEARCH_API_KEY; result count, source selection, and reranking are controlled by command-line options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
