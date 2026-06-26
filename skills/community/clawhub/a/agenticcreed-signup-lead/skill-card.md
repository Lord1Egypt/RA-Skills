## Description: <br>
Create a new signup lead in AgenticCreed by submitting contact and personal details via the public HTTP API endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waqas-orcalo](https://clawhub.ai/user/waqas-orcalo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and operators use this skill to create AgenticCreed signup leads after the user confirms the lead details to submit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits personal signup lead details, including contact information and optional sensitive fields, to AgenticCreed. <br>
Mitigation: Confirm the user wants to send the listed fields before each use, omit optional sensitive fields unless needed, and use a protected, least-privilege API key. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/waqas-orcalo/agenticcreed-signup-lead) <br>
- [AgenticCreed Signup Leads API Endpoint](https://gateway.agenticcreed.ai/signup-leads) <br>


## Skill Output: <br>
**Output Type(s):** [API call, JSON response, Configuration] <br>
**Output Format:** [HTTP POST request with JSON response mapping] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTICCREED_API_KEY and user-confirmed lead fields before submission.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
