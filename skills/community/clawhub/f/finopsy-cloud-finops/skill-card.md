## Description:

Analyze and optimize cloud costs across AWS, Azure, and GCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operations teams, and finance stakeholders use this skill to request AWS, Azure, or GCP cost analysis, spending trends, rightsizing recommendations, unused resource detection, and savings estimates through the ToolWeb Finopsy API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to send reusable cloud credentials to a third-party paid API.

Mitigation: Use dedicated, least-privilege, read-only, short-lived credentials; avoid root, admin, owner, or broad service-account credentials; rotate or revoke credentials after use.

Risk: Retention, logging, pricing, and privacy terms for the third-party API may affect user data and cost exposure.

Mitigation: Confirm ToolWeb.in retention, logging, pricing, and privacy terms before providing credentials or running paid API calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/finopsy-cloud-finops)
- [ToolWeb Portal](https://portal.toolweb.in)
- [Finopsy API Endpoint](https://portal.toolweb.in/apis/tools/finopsy)
- [ToolWeb Platform](https://toolweb.in)
- [ToolWeb OpenClaw Skills](https://toolweb.in/openclaw/)
- [ToolWeb MCP Server](https://hub.toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown cost analysis report with curl-based API invocation guidance and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, TOOLWEB_API_KEY, and user-provided cloud provider credentials for AWS, Azure, or GCP.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
