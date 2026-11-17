## Description:

Build targeted company lists for outbound campaigns using Extruct.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkid18](https://clawhub.ai/user/zkid18)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, and GTM users use this skill to turn ICP context, seed companies, and campaign goals into targeted company search strategies and outbound account lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read GTM context files containing ICPs, win cases, DNC domains, customers, or partners, and may send company domains to Extruct through the companion API skill.

Mitigation: Review the context file and data-sharing expectations before use, remove DNC domains before upload, and send only approved company domains to Extruct.

Risk: The workflow depends on the companion extruct-api skill for searches, table creation, uploads, and enrichment runs.

Mitigation: Confirm the extruct-api skill is installed and configured before running list-building workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zkid18/skills/extruct-list-building)
- [ClawHub publisher profile](https://clawhub.ai/user/zkid18)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with delegated Extruct API operations and optional table link or CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read GTM context files and delegate search, table creation, upload, and enrichment operations to the companion extruct-api skill.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
