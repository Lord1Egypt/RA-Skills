## Description:

ApiTest retrieves tool information from a local localhost:8080/gettool endpoint using a Bearer token from API_TEST_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yehan5555](https://clawhub.ai/user/yehan5555)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let an agent fetch tool data from a trusted local service after configuring API_TEST_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send API_TEST_KEY as a Bearer token to localhost:8080.

Mitigation: Use it only with an intentionally running, trusted localhost:8080 service and require confirmation before sending the token.

Risk: Broad auto-invocation patterns may trigger authenticated requests for loosely related API or localhost requests.

Mitigation: Narrow triggers to the exact gettool request or disable automatic invocation.

Risk: The credential is described as read-write.

Mitigation: Provide a narrowly scoped or read-only credential whenever the local service supports it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yehan5555/skills/apitest)
- [Publisher profile](https://clawhub.ai/user/yehan5555)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional JSON response data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API_TEST_KEY and a trusted service on localhost:8080.]

## Skill Version(s):

1.0.2 (source: server release metadata and skill frontmatter name)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
