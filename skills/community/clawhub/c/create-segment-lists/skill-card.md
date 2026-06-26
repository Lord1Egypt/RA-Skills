## Description: <br>
Create business segment lists in HubSpot for customers, partners, competitors, employees, ICP tiers, and industries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, RevOps, and CRM operators use this skill to plan, create, verify, and maintain HubSpot contact segment lists for targeting, suppression, and analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HubSpot list creation may group contacts incorrectly if list names, criteria, or source properties are wrong. <br>
Mitigation: Review the exact list names and criteria before creation, use a least-privilege HubSpot private app token, and verify member counts after creation. <br>
Risk: New segment lists could affect campaigns, workflows, or suppression behavior before they are checked. <br>
Mitigation: Do not connect new lists to campaigns or workflows until reviewed, and check dependencies before deleting or replacing lists. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomgranot/create-segment-lists) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with HubSpot list criteria and a Python API example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes interview prompts, recommended segment definitions, verification checks, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
