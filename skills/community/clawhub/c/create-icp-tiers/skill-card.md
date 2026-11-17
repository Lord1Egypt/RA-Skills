## Description:

Classify companies into Ideal Customer Profile (ICP) tiers based on firmographic data (industry + employee count). Creates a custom property via API and 4 classification workflows in HubSpot UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations, sales operations, and CRM administrators use this skill to create and validate HubSpot ICP tiering based on industry and employee-count criteria. It helps prioritize companies for sales and marketing workflows while preserving an audit trail before and after classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow setup can persistently update ICP tier values across all HubSpot company records.

Mitigation: Test in a HubSpot sandbox or small filtered cohort, export affected company data first, and define rollback steps before enrolling all existing companies.

Risk: Broad administrator access or long-lived mutation tokens could increase the impact of mistakes or credential exposure.

Mitigation: Avoid Super Admin where possible, use separate least-privileged tokens for audit and mutation steps, and rotate the mutation token after setup.

Risk: Incorrect HubSpot workflow triggers can misclassify companies or overwrite higher-priority tiers.

Mitigation: Manually verify filter-based AND trigger logic, re-enrollment settings, and staggered activation before turning workflows on broadly.

## Reference(s):

- [Create Icp Tiers on ClawHub](https://clawhub.ai/tomgranot/skills/create-icp-tiers)
- [HubSpot API](https://api.hubapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python scripts and HubSpot configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces before-state and after-state CSV audit files when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
