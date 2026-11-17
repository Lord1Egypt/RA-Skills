## Description:

Semantic search, web scraping, and content extraction optimized for AI agents and LLMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research agents use this skill to run Exa semantic web searches, extract clean Markdown from pages, collect highlights, and discover pages similar to a source URL for retrieval and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, URLs, and extracted content may be sent to Exa as an external provider.

Mitigation: Configure EXA_API_KEY only when Exa use is intended, and avoid sending secrets, private internal URLs, proprietary topics, or regulated data unless organizational policy allows Exa processing.

## Reference(s):

- [API Reference](references/api_reference.md)
- [Exa API Documentation](https://docs.exa.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the external Exa API using EXA_API_KEY and can request live crawling or cached content depending on max_age_hours.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
