## Description:

Fetch public Weibo posts, profiles, comments, and trends through DataXAPI, with per-call pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents querying public Weibo content use this skill to look up posts, profiles, comments, and current trends through DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery requests may send the user's wording to DataXAPI.

Mitigation: Avoid including sensitive details in discovery requests and make the external request clear to the user.

Risk: The package installation instructions do not pin a version.

Mitigation: Review the package source and pin a trusted version before installing.

## Reference(s):

- [DataXAPI Weibo API documentation](https://dataxapi.com/apis/weibo/)
- [DataXAPI Weibo pricing](https://dataxapi.com/pricing/weibo/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-weibo)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured JSON data with concise user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are public Weibo data; calls require a DataXAPI key and are charged per call.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
