## Description:

Perform web searches using Alibaba Cloud UnifiedSearch API. Provides advanced search capabilities with configurable parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leowing](https://clawhub.ai/user/leowing)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Alibaba Cloud UnifiedSearch queries and return formatted web search results with optional filters for engine type, time range, category, city, and IP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials could be exposed or granted broader permissions than the search task requires.

Mitigation: Store credentials in environment variables or a managed secret store, grant only the permissions needed for UnifiedSearch, and rotate keys according to local policy.

Risk: Search queries and optional city or IP parameters are sent to Alibaba Cloud.

Mitigation: Avoid sensitive queries or location parameters unless that data sharing is acceptable for the deployment context.

Risk: Dependency installation can introduce unreviewed package versions.

Mitigation: Install in a virtual environment, pin reviewed dependency versions, and remove the unused requests dependency if possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leowing/skills/aliyun-search-1-0-0)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text search results and Markdown setup/usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include titles, links, snippets, and published times.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
