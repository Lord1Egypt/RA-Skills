## Description:

Query Bangumi (bgm.tv) for anime, manga, light novels, games, and music. Search subjects, view details and episode lists, browse seasonal anime charts, rating rankings, and look up voice actors / staff. No authentication required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mountlynx](https://clawhub.ai/user/mountlynx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Bangumi subjects, inspect anime and media details, browse seasonal charts and rankings, and look up people or characters without authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes unauthenticated requests to the Bangumi API.

Mitigation: Use it only where outbound requests to Bangumi are acceptable, and review returned information before relying on it.

Risk: Fetched query and result data may be cached locally in ~/.bangumi/cache/.

Mitigation: Avoid shared machines for sensitive lookups, or clear the cache directory after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mountlynx/skills/bangumi-explorer)
- [Bangumi API base](https://api.bgm.tv/v0)
- [Bangumi API documentation](https://github.com/bangumi/api)
- [Bangumi OpenAPI specification](https://github.com/bangumi/api/blob/master/open-api/v0.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill returns Bangumi search results, details, episode lists, seasonal charts, rankings, person records, calendar entries, or character records as concise text.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
