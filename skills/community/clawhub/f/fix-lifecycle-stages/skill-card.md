## Description: <br>
Ensures contacts and companies have appropriate lifecycle stages by backfilling missing values, correcting disallowed stages, and creating prevention workflows to stop future gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Revenue operations and CRM administrators use this skill to audit and repair HubSpot lifecycle stage data for contacts and companies, then add workflows that reduce future lifecycle-stage gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk edits can change HubSpot contact and company lifecycle stages at scale. <br>
Mitigation: Export affected records, test on a small sample, review the disallowed-stage mapping for the tenant, and keep a rollback plan before running update scripts. <br>
Risk: Prevention workflows can continue applying default lifecycle stages after the cleanup. <br>
Mitigation: Review workflow enrollment and re-enrollment settings before activation, then monitor initial runs for unintended stage changes. <br>
Risk: Incorrect lifecycle-stage mappings can degrade funnel reporting and segmentation. <br>
Mitigation: Define tenant-specific mappings and spot-check records associated with customer and opportunity companies before applying broad changes. <br>


## Reference(s): <br>
- [ClawHub release: Fix Lifecycle Stages](https://clawhub.ai/tomgranot/fix-lifecycle-stages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code blocks and workflow configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundled scripts can produce CSV audit trails when run against HubSpot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
