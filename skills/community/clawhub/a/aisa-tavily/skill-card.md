## Description:

Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, research-ready outputs, and structured retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run AIsa-backed web research, recent-news searches, multi-source retrieval, competitor scans, trend discovery, and URL content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and supplied URLs are sent to AIsa as a third-party research provider.

Mitigation: Do not submit private document links, localhost or internal URLs, secret-bearing query strings, or sensitive searches unless sharing them with AIsa is intended.

Risk: Some providers or URLs may fail or time out, which can make research output incomplete.

Mitigation: Report failed providers or URLs clearly and do not claim sources that were not actually queried.

## Reference(s):

- [AIsa Tavily on ClawHub](https://clawhub.ai/bibaofeng/skills/aisa-tavily)
- [bibaofeng ClawHub publisher profile](https://clawhub.ai/user/bibaofeng)
- [AIsa Tavily search API endpoint](https://api.aisa.one/apis/v1/tavily/search)
- [AIsa Tavily extract API endpoint](https://api.aisa.one/apis/v1/tavily/extract)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with source lists, extracted content, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and AISA_API_KEY for AIsa-backed search and extraction requests.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
