## Description:

Look up Feishu Open API documentation for endpoint discovery, parameter and response details, API-calling scripts, and troubleshooting Feishu API errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to find Feishu Open Platform API documentation, identify endpoints, understand request and response formats, and draft or troubleshoot scripts that call Feishu APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to access local Feishu app credentials and request tenant access tokens.

Mitigation: Use placeholders or a dedicated secret manager, avoid exposing local credential files to the agent, and require explicit user confirmation before token requests.

Risk: Authenticated Feishu API calls may affect tenant data, including write-capable operations.

Mitigation: Review requested API scopes and require explicit confirmation before any write-capable or tenant-affecting Feishu API call.

## Reference(s):

- [Feishu message create API documentation](https://open.feishu.cn/document/server-docs/im-v1/message/create)
- [Feishu Apifox documentation mirror](https://feishu.apifox.cn)
- [ClawHub skill release page](https://clawhub.ai/deadblue22/skills/feishu-api-lookup)
- [Publisher profile](https://clawhub.ai/user/deadblue22)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API endpoint summaries and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu HTTP methods, paths, headers, request bodies, response fields, error codes, required permissions, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
