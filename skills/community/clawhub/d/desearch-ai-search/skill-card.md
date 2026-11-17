## Description:

AI-powered search that aggregates and summarizes results from multiple sources including web, X/Twitter, Reddit, Hacker News, YouTube, ArXiv, and Wikipedia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okradze](https://clawhub.ai/user/okradze)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Desearch-powered research queries, retrieve curated links, and summarize results across web, social, video, academic, and wiki sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts and requested topics are sent to Desearch as a third-party search provider.

Mitigation: Avoid submitting private or sensitive queries unless they are intended to be processed by Desearch.

Risk: The skill requires a Desearch API key for access.

Mitigation: Store DESEARCH_API_KEY as a secret or environment variable and do not hardcode it in shared files.

## Reference(s):

- [Skill release page](https://clawhub.ai/okradze/skills/desearch-ai-search)
- [Desearch homepage](https://desearch.ai)
- [Desearch API reference](https://desearch.ai/docs/api-reference/post-desearch-ai-search)
- [Desearch Console](https://console.desearch.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text or JSON search results with links, snippets, tweets, and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DESEARCH_API_KEY and sends search prompts to the Desearch API.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
