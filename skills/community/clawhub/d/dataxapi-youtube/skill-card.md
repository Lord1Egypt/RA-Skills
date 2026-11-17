## Description:

Retrieves public YouTube video, channel, post, comment, and transcript data through DataXAPI for user questions or supplied YouTube links and IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up public YouTube videos, channels, posts, comments, and transcripts when answering questions or working from a YouTube link, ID, or channel name. Calls are paid from a prepaid DataXAPI balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms are sent to DataXAPI, and successful calls use a prepaid balance.

Mitigation: Send only the YouTube details needed for the request, check pricing, and set a per-call spending limit.

Risk: The API key authorizes paid requests, and the optional CLI depends on downloaded npm code.

Mitigation: Protect DATAXAPI_API_KEY and prefer REST or a reviewed, pinned CLI version.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [YouTube API documentation](https://dataxapi.com/apis/youtube/)
- [YouTube pricing](https://dataxapi.com/pricing/youtube/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured public YouTube data with agent-written summaries or answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result page per call; additional pages are separate paid calls.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
