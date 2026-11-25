## Description:

Search Xiaohongshu notes by keyword and retrieve selected notes' full text, with engagement metrics and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can research topics, compare competitor posts, find highly liked or saved notes, and review product posts on Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags an unpinned third-party `dataxapi` command-line dependency.

Mitigation: Review the package and pin the `dataxapi` version before installing or running it.

Risk: Calls may forward pasted share text or token-bearing note URLs to DataXAPI.

Mitigation: Avoid sending sensitive share text or token-bearing URLs, and use only inputs you are comfortable sharing with DataXAPI.

Risk: The security analysis is incomplete because some local references could not be resolved.

Mitigation: Review the skill and its dependency before installation.

## Reference(s):

- [DataXAPI homepage](https://dataxapi.com)
- [Xiaohongshu notes search API documentation](https://dataxapi.com/apis/xiaohongshu/notes/search/)
- [Xiaohongshu note details API documentation](https://dataxapi.com/apis/xiaohongshu/notes/get/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured note search results and note details with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search filters and paging are available; each search or detail call costs $0.02 according to the skill documentation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
