## Description:

Fetch public Instagram posts, hashtags, user profiles, comments, and transcripts through DataXAPI's eight per-call priced endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up public Instagram profiles, posts, hashtag results, comments, replies, and short video transcripts, then answer questions with the returned data and its source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint discovery may send the user's wording to DataXAPI.

Mitigation: Avoid including sensitive or identifying details in discovery queries; use only the minimum wording needed to find an endpoint.

Risk: The documented `npx dataxapi` invocation is unpinned and may download a package at runtime.

Mitigation: Review the package and pin a version before running it, or use an installation method whose version has already been reviewed.

## Reference(s):

- [DataXAPI Instagram API catalog](https://dataxapi.com/apis/instagram/)
- [Instagram API pricing](https://dataxapi.com/pricing/instagram/)
- [DataXAPI agent setup documentation](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON data with concise Markdown answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each page requires a separate call; tell the user the price before calls that add up and set a maximum price.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
