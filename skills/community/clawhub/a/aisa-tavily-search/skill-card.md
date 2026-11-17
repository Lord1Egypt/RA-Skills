## Description:

Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run current web research, extract supplied URLs, compare tools or companies, and turn retrieved sources into concise research briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and supplied URLs are sent to AIsa/Tavily using the configured API key.

Mitigation: Avoid submitting secrets, private internal documents, regulated personal data, or queries that must remain local.

Risk: Web search and extraction results can be incomplete, stale, or affected by provider timeouts.

Mitigation: Report missing or failed providers clearly and verify important claims against the returned sources before relying on them.

## Reference(s):

- [AIsa homepage](https://aisa.one)
- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/aisa-tavily-search)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style research summaries, source lists, and extracted page text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and Node.js; search result counts are capped by the bundled script.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
