## Description:

Generate a comprehensive DPDP Act implementation checklist with evidence tracker and roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, privacy teams, and compliance leads use this skill to gather organization context and request a DPDP Act implementation checklist, roadmap, evidence tracker, and executive summary from ToolWeb.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organization DPDP planning details to ToolWeb's external API.

Mitigation: Minimize submitted data and avoid secrets, customer records, incident details, unnecessary personal names, or other sensitive information; use pseudonymous values where possible.

Risk: Successful API calls may consume paid quota or incur billing.

Mitigation: Confirm TOOLWEB_API_KEY configuration and expected paid API use before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/dpdp-checklist-gen)
- [ToolWeb API Portal](https://portal.toolweb.in)
- [ToolWeb Platform](https://toolweb.in)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary of checklist, roadmap, evidence tracker, and executive summary content returned by the ToolWeb API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may be metered or billed by ToolWeb.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
