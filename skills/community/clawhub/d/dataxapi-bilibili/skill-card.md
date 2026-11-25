## Description:

Public Bilibili data through DataXAPI: videos, users, comments, and trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve public Bilibili video, user, comment, and trending data through DataXAPI. It helps answer questions about Bilibili content, accounts, comments, and current trends using endpoint-specific, pay-per-call requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended npm package command is unpinned, so package updates could change what runs.

Mitigation: Prefer a reviewed, pinned package version when available.

Risk: The security analysis is partial because some local path-like references could not be resolved.

Mitigation: Review the package and its referenced files before granting it access to the DataXAPI key.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [Bilibili API reference](https://dataxapi.com/apis/bilibili/)
- [Bilibili pricing](https://dataxapi.com/pricing/bilibili/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON API data with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paged results; each API request incurs the endpoint's listed charge.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
