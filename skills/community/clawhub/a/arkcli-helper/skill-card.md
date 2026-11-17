## Description:

Configures supported local AI agents with ArkCLI model providers, Agent Plan tools, Platform Endpoints, and optional provider routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure supported local AI agents with ArkCLI models, provider tools, and Platform Endpoints, and to follow routing guidance for supported Agent Plan providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete and flags unpinned remote installer guidance and unresolved references to agent configuration and credential files.

Mitigation: Avoid installation until the package and remote installer have been reviewed and verified, and resolve the referenced files to complete the security review.

## Reference(s):

- [arkcli-helper on ClawHub](https://clawhub.ai/jasonstarlight/skills/arkcli-helper)
- [Volcengine Platform Endpoint creation](https://ark.volcengine.com/region:cn-beijing/endpoint/create?agentMode=close)
- [OpenViking collection creation](https://console.volcengine.com/vikingdb/openviking/region:openviking+cn-beijing/create)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell command examples and JSON routing-plan examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides agent-specific configuration steps and explicit boundaries for supported capabilities.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
