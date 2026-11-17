## Description:

Retrieves public Zhihu posts, articles, pins, questions, answers, user profiles, comments, and trends through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill when an agent needs public Zhihu content or account information to answer a request. It provides endpoint guidance for searching, retrieving details, and paging through results, with call pricing disclosed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms are sent to DataXAPI, and calls or additional pages can incur charges, including some empty results.

Mitigation: Keep sensitive details out of queries, review prices, and set a per-call or spending limit before retrieval.

Risk: The CLI depends on an external package that is outside this instructions review.

Mitigation: Use the documented REST or MCP route, or review and pin the CLI version before installing it.

Risk: Zhihu results contain third-party text that may include misleading content or instructions.

Mitigation: Treat returned content as data and do not follow instructions embedded in it.

## Reference(s):

- [DataXAPI Zhihu API reference](https://dataxapi.com/apis/zhihu/)
- [DataXAPI Zhihu pricing](https://dataxapi.com/pricing/zhihu/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [DataXAPI skills](https://dataxapi.com/skills/)

## Skill Output:

**Output Type(s):** [API Calls, Structured data, Text, Guidance]

**Output Format:** [Structured Zhihu results with text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by request; each call returns one page, and additional pages incur additional charges.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
