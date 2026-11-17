## Description:

Search, book, and manage scientific research equipment at 200+ institutions with real-time availability, service requests, and collaborator discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cesco345](https://clawhub.ai/user/cesco345)

### License/Terms of Use:


## Use Case:

External researchers and lab operations teams use this skill to find scientific instruments, check availability, reserve equipment time, submit service requests, and discover collaborators across shared research facilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act on equipment bookings and service requests after OAuth authorization.

Mitigation: Confirm trust in capneteq.com and review requested OAuth scopes before authorizing booking or service-request access.

Risk: Optional proactive automations may monitor saved searches, bookings, pricing, availability, and collaborator profiles.

Mitigation: Enable only the automations needed for the workflow and keep them disabled when periodic monitoring is not desired.

## Reference(s):

- [Capital Equipment ClawHub listing](https://clawhub.ai/cesco345/skills/capneteq-cesco345)
- [Capital Equipment MCP endpoint](https://capneteq.com/mcpServer/mcp)
- [Publisher profile](https://clawhub.ai/user/cesco345)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, API Calls]

**Output Format:** [Markdown and conversational text with configuration examples and MCP-mediated actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OAuth 2.1 authorization for equipment read, booking, service-request, and profile access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
