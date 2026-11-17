## Description:

Bimiyun Search lets an agent query the Bimiyun web search API and return LLM-friendly results as Markdown or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bimiyun888](https://clawhub.ai/user/bimiyun888)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill when an agent needs to search the web through Bimiyun and return readable or structured results. It supports language, result count, safe search, search mode, and output format options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are transmitted to Bimiyun.

Mitigation: Do not submit sensitive or confidential queries, and install the skill only in environments where sending search terms to Bimiyun is acceptable.

Risk: Supplying the API key on the command line can expose it through shell history or process listings.

Mitigation: Provide BIMIYUN_API_KEY through a trusted secret store or environment variable instead of using --api-key.

Risk: BIMIYUN_ENDPOINT can redirect requests and expose the API key to another destination.

Mitigation: Leave BIMIYUN_ENDPOINT unset unless the alternate endpoint is fully trusted and intended.

Risk: Broad search-trigger language can cause the skill to be invoked more often than intended.

Mitigation: Use explicit invocation or review agent routing rules before deploying the skill in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bimiyun888/skills/bimiyun-search)
- [Bimiyun website](https://bimiyun.com)
- [Bimiyun web search API endpoint](https://search.bimiyun.com/api/web)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BIMIYUN_API_KEY; supports 1-10 results, optional language selection, safe search, and fulltext or snippet mode.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
