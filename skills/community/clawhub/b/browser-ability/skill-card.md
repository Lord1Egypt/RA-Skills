## Description:

This skill enables an AI Agent to signin and retrieve data from websites via JS script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[faisalive](https://clawhub.ai/user/faisalive)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to list and call MCP browser tools for websites that may require user sign-in. It supports a manual sign-in handoff, then resumes the requested data retrieval with a signin_id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives a configured MCP server raw browser-control access through a CDP endpoint.

Mitigation: Only install it when the MCP server is trusted and CDP is bound to a protected local interface.

Risk: Transport and configuration details are weakly disclosed, including SERVER_URL expectations.

Mitigation: Document SERVER_URL, enforce trusted HTTPS destinations, and avoid sending raw CDP endpoints to remote services.

Risk: The sign-in guidance is conflicting for sensitive accounts.

Mitigation: Resolve the sign-in instructions before using the skill with sensitive accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/faisalive/skills/browser-ability)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sign-in URLs, signin_id values, and JSON returned by MCP tools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
