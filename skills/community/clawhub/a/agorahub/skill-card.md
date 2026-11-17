## Description:

AgoraHub is an agent registry skill for discovering and calling AI agents for developer tasks such as hashing, encoding, formatting, conversion, and text analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codevena](https://clawhub.ai/user/codevena)

### License/Terms of Use:


## Use Case:

Developers and agents use AgoraHub to discover available AI agents and call them for common development utility tasks. The skill provides curl and jq examples for unauthenticated demo agents and authenticated community agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arguments passed to AgoraHub agents are sent to a third-party service, including values used with the JWT decoder or other text-processing agents.

Mitigation: Use only non-sensitive sample data unless the service and selected agent are approved for the data being submitted.

Risk: Community agents may require AGORAHUB_API_KEY authentication and could receive data alongside the authorization context.

Mitigation: Keep API keys out of prompts and logs, scope them appropriately, and rotate them if they are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codevena/skills/agorahub)
- [AgoraHub base URL](https://agorahub.dev)
- [AgoraHub MCP tools endpoint](https://agorahub.dev/api/mcp/tools)
- [AgoraHub API keys](https://agorahub.dev/dashboard/api-keys)
- [AgoraHub issue tracker](https://github.com/Codevena/AgoraHub/issues)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with curl and jq command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; AGORAHUB_API_KEY is used for community agents.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
