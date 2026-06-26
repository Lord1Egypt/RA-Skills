## Description: <br>
Classify companies into Ideal Customer Profile (ICP) tiers based on firmographic data (industry + employee count). Creates a custom property via API and 4 classification workflows in HubSpot UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, and CRM operations teams use this skill to define ICP tier criteria, create a HubSpot company property, and set up workflows that keep company records classified for lead prioritization and campaign segmentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses HubSpot API access to create and verify a CRM-wide company property. <br>
Mitigation: Confirm the target HubSpot portal first and use a minimally scoped HubSpot private app token. <br>
Risk: Incorrect property names, tier criteria, or workflow activation order can cause broad misclassification of company records. <br>
Mitigation: Review the property name, tier rules, and staggered workflow activation sequence before enabling workflows, then verify classification results before relying on them. <br>
Risk: HubSpot Breeze AI may create event-based triggers or omit required guards, which can assign tiers incorrectly. <br>
Mitigation: Manually verify workflow triggers use filter-based AND logic, include the ICP Tier unknown guard where required, and have re-enrollment configured. <br>


## Reference(s): <br>
- [Create Icp Tiers ClawHub listing](https://clawhub.ai/tomgranot/create-icp-tiers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python scripts and HubSpot workflow configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CRM setup guidance and audit outputs for HubSpot company ICP tier classification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
