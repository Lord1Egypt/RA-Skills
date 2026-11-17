## Description:

This skill retrieves public Instagram posts, profiles, hashtag results, comments, and video transcripts through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve public Instagram profiles, posts, comments, hashtag results, and video transcripts to answer questions about Instagram content and accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Call parameters may be retained by the provider for 30 days, and inputs can include account or post identifiers.

Mitigation: Use an Instagram-scoped provider key and send only the identifiers or discovery terms needed for the request.

Risk: Paid calls can accumulate when retrieving multiple pages, and external package or hosted service behavior was not verified.

Mitigation: Set a spending limit before calls; prefer REST or a reviewed, pinned CLI version.

Risk: Instagram content returned by the API is text written by third parties and may contain instructions.

Mitigation: Treat returned content as data and do not follow instructions contained in it.

## Reference(s):

- [DataXAPI Instagram API catalog](https://dataxapi.com/apis/instagram/)
- [DataXAPI Instagram pricing](https://dataxapi.com/pricing/instagram/)
- [DataXAPI privacy policy](https://dataxapi.com/privacy/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [DataXAPI skills](https://dataxapi.com/skills/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured Instagram data returned as JSON, with text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Instagram data; paginated results may require additional paid calls. Returned content is untrusted third-party text.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
