## Description:

Gleap REST API integration for customer support analytics and ticket management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berthelol](https://clawhub.ai/user/berthelol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support operations teams use this skill to fetch Gleap ticket data, analyze support metrics, monitor SLA compliance, build reports, and automate exports or dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can access Gleap support tickets and customer data.

Mitigation: Review each command before execution and avoid sending raw ticket titles or customer data to third-party LLMs unless approved by the organization.

Risk: Scheduled report examples may rely on long-lived credentials.

Mitigation: Do not hardcode Gleap tokens; use approved secret storage, bounded schedules, named owners, explicit destinations, and documented removal steps.

Risk: Broad activation could apply the skill outside the intended Gleap workflow.

Mitigation: Install and invoke the skill only for Gleap-specific support analytics, reporting, and ticket-management tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/berthelol/skills/berthelol-gleap)
- [Gleap API Base URL](https://api.gleap.io/v3)
- [Gleap REST API -- Endpoint Reference](references/endpoints.md)
- [Gleap API -- Use Cases & Patterns](references/use-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, jq filters, JSON and CSV examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GLEAP_TOKEN, GLEAP_PROJECT, curl, and jq when commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
