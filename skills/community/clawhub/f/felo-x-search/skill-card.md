## Description:

Search X (Twitter) data using Felo X Search API for user lookup, user search, user tweets, tweet search, and tweet replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search X/Twitter users, tweets, timelines, and replies through the Felo X Search API from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the Felo API key to a custom API base URL if FELO_API_BASE is set or influenced.

Mitigation: Keep FELO_API_BASE unset unless the endpoint is controlled and trusted, and use a revocable or limited-scope Felo API key where possible.

Risk: The artifact recommends an unpinned global npm install path.

Mitigation: Prefer the bundled script, or pin and review the package version before using a global install.

## Reference(s):

- [Felo X Search API](https://openapi.felo.ai/docs/api-reference/v2/x-search.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/felo-x-search)
- [Publisher profile](https://clawhub.ai/user/wangzhiming1999)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summaries by default, raw JSON when requested, and setup or error guidance as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FELO_API_KEY and supports query, id, user mode, tweet mode, limit, cursor, time filters, timeout, and JSON-output options.]

## Skill Version(s):

1.0.1 (source: evidence release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
