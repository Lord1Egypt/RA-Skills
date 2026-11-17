## Description:

Fetches current library documentation through the Context7 API so agents can answer library questions and work with library-dependent code using fresher API context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[am-will](https://clawhub.ai/user/am-will)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to search for libraries and fetch targeted Context7 documentation before implementing, debugging, or answering questions about third-party package APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The distributed source includes a bearer token for the Context7 API.

Mitigation: Remove the bundled key and require users to provide their own credential through the CONTEXT7_API_KEY environment variable or another secure secret mechanism.

Risk: Library names and documentation queries are sent to Context7 by design.

Mitigation: Disclose the external network call and avoid sending secrets, proprietary identifiers, or sensitive implementation details in documentation search terms.

Risk: The skill encourages broad proactive use of the external service.

Mitigation: Scope invocation to explicit documentation lookup needs or request user confirmation in sensitive workspaces.

## Reference(s):

- [Context7 API endpoint](https://context7.com/api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Context7 API responses printed as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The context command supports a response token limit and text or JSON output selection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
