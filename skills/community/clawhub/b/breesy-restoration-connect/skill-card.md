## Description: <br>
Submit customer-authorized property damage restoration help requests for water, fire, mold, storm, biohazard, and reconstruction services across the United States. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyle-breesy](https://clawhub.ai/user/kyle-breesy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customers or assisting agents use this skill to submit customer-authorized restoration service requests for property damage. It supports water, fire, smoke, mold, storm, biohazard, and reconstruction request workflows across the United States. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Submitting a restoration request shares customer contact, location, service type, urgency, and damage details with Breesy Restoration Connect or its restoration partners. <br>
Mitigation: Submit only after the customer authorizes contact and verify the phone number, location, service type, urgency, and damage details before sending. <br>
Risk: Retrying a request without a stable retry key could create duplicate service requests. <br>
Mitigation: Use idempotencyKey when retrying the same customer request. <br>


## Reference(s): <br>
- [Breesy Connect Homepage](https://breesy-connect.com) <br>
- [OpenAPI Specification](https://breesy-connect.com/openapi.json) <br>
- [Agent Instructions](https://breesy-connect.com/llms.txt) <br>
- [Agent Manifest](https://breesy-connect.com/.well-known/agent.json) <br>
- [Agent Card](https://breesy-connect.com/.well-known/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with JSON-compatible API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit customer consent before submission; use idempotencyKey when retrying the same customer request.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
